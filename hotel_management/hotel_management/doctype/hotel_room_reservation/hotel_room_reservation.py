# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, json
from frappe.model.document import Document
from frappe import _, msgprint
from frappe.utils import date_diff, add_days, flt
from frappe.desk.reportview import get_match_cond, get_filters_cond
from frappe.utils import nowdate



class HotelRoomUnavailableError(frappe.ValidationError): pass
class HotelRoomPricingNotSetError(frappe.ValidationError): pass

class HotelRoomReservation(Document):
	def validate(self):
		self.total_rooms = {}
		self.set_rates()
		self.validate_availability()

	def on_submit(self):
		room = frappe.get_doc('Hotel Room', self.hotel_room)
		room.set('status', 'Booked')
		room.db_update()


	def validate_availability(self):
		for i in range(date_diff(self.to_date, self.from_date)):
			day = add_days(self.from_date, i)
			self.rooms_booked = {}

			for d in self.items:
				if not d.item in self.rooms_booked:
					self.rooms_booked[d.item] = 0

				room_type = frappe.db.get_value("Hotel Room Package",
					d.item, 'hotel_room_type')
				rooms_booked = get_rooms_booked(room_type, day, exclude_reservation=self.name) \
					+ d.qty + self.rooms_booked.get(d.item)
				total_rooms = self.get_total_rooms(d.item)
				self.get_all_rooms(d.item)
				if total_rooms < rooms_booked:
					frappe.throw(_("Hotel Rooms of type {0} are unavailable on {1}".format(d.item,
						frappe.format(day, dict(fieldtype="Date")))), exc=HotelRoomUnavailableError)

				self.rooms_booked[d.item] += rooms_booked

	def get_total_rooms(self, item):
		if not item in self.total_rooms:
			self.total_rooms[item] = frappe.db.sql("""
				select count(*)
				from
					`tabHotel Room Package` package
				inner join
					`tabHotel Room` room on package.hotel_room_type = room.hotel_room_type
				where
					package.item = %s""", item)[0][0] or 0

		return self.total_rooms[item]

	def get_all_rooms(self, item):
		total_rooms = {}
		if not item in total_rooms:
				total_rooms[item] = frappe.db.sql("""
					select room.name
					from
						`tabHotel Room` room
					inner join
						`tabHotel Room Package` package on room.hotel_room_type=package.hotel_room_type
					where
						package.item = %s""", item)[0][0] or 0
		# msgprint(_(total_rooms[item]))

		return total_rooms[item]

	def set_rates(self):
		self.net_total = 0
		for d in self.items:
			net_rate = 0.0
			for i in range(date_diff(self.to_date, self.from_date)):
				day = add_days(self.from_date, i)
				if not d.item:
					continue
				day_rate = frappe.db.sql("""
					select 
						item.rate 
					from 
						`tabHotel Room Pricing Item` item,
						`tabHotel Room Pricing` pricing
					where
						item.parent = pricing.name
						and item.item = %s
						and %s between pricing.from_date 
							and pricing.to_date""", (d.item, day))

				if day_rate:
					net_rate += day_rate[0][0]
				else:
					frappe.throw(
						_("Please set Hotel Room Rate on {}".format(
							frappe.format(day, dict(fieldtype="Date")))), exc=HotelRoomPricingNotSetError)
			d.rate = net_rate
			d.amount = net_rate * flt(d.qty)
			self.net_total += d.amount

@frappe.whitelist()
def get_room_rate(hotel_room_reservation):
	"""Calculate rate for each day as it may belong to different Hotel Room Pricing Item"""
	doc = frappe.get_doc(json.loads(hotel_room_reservation))
	doc.set_rates()
	return doc.as_dict()

def get_rooms_booked(room_type, day, exclude_reservation=None):
	exclude_condition = ''
	if exclude_reservation:
		exclude_condition = 'and reservation.name != "{0}"'.format(frappe.db.escape(exclude_reservation))

	return frappe.db.sql("""
		select sum(item.qty)
		from
			`tabHotel Room Package` room_package,
			`tabHotel Room Reservation Item` item,
			`tabHotel Room Reservation` reservation
		where
			item.parent = reservation.name
			and room_package.item = item.item
			and room_package.hotel_room_type = %s
			and reservation.docstatus = 1
			{exclude_condition}
			and %s between reservation.from_date
				and reservation.to_date""".format(exclude_condition=exclude_condition), 
				(room_type, day))[0][0] or 0

def get_rooms_name_booked(room_type, day, exclude_reservation=None):
	exclude_condition = ''
	if exclude_reservation:
		exclude_condition = 'and reservation.name != "{0}"'.format(frappe.db.escape(exclude_reservation))

	return frappe.db.sql("""
		select sum(item.qty)
		from
			`tabHotel Room Package` room_package,
			`tabHotel Room Reservation Item` item,
			`tabHotel Room Reservation` reservation
		where
			item.parent = reservation.name
			and room_package.item = item.item
			and room_package.hotel_room_type = %s
			and reservation.docstatus = 1
			{exclude_condition}
			and %s between reservation.from_date
				and reservation.to_date""".format(exclude_condition=exclude_condition),
						 (room_type, day))[0][0] or 0


@frappe.whitelist()
def release_room(hotel_room):
	room = frappe.get_doc('Hotel Room', hotel_room)
	# TODO (do verification first)
	room.set('status', 'Available')
	room.db_update()
	msgprint(_("Room" + "  " + hotel_room + " " + "Has been Released"))


def get_packages_list(hotel_room):
	if not hotel_room:
		frappe.throw(_('Please select a Room'))
	room_type = frappe.db.get_value('Hotel Room', hotel_room, 'hotel_room_type')
	return room_type

@frappe.whitelist()
def item_query_room(doctype='Item', txt='', searchfield='name', start=0, page_len=20, filters=None, as_dict=False):
	'''Return items that are selected in active menu of the restaurant'''
	hotel_type = get_packages_list(filters['hotel_room'])
	# frappe.msgprint(_(hotel_type))
	items = frappe.db.get_all('Hotel Room Package', ['item'], dict(hotel_room_type = hotel_type))
	# frappe.msgprint(_(items))
	del filters['hotel_room']
	filters['name'] = ('in', [d.item for d in items])

	return item_query('Item', txt, searchfield, start, page_len, filters, as_dict)

def item_query(doctype, txt, searchfield, start, page_len, filters, as_dict=False):
	conditions = []

	description_cond = ''
	if frappe.db.count('Item', cache=True) < 50000:
		# scan description only if items are less than 50000
		description_cond = 'or tabItem.description LIKE %(txt)s'

	return frappe.db.sql("""select tabItem.name,
		if(length(tabItem.item_name) > 40,
			concat(substr(tabItem.item_name, 1, 40), "..."), item_name) as item_name,
		tabItem.item_group,
		if(length(tabItem.description) > 40, \
			concat(substr(tabItem.description, 1, 40), "..."), description) as decription
		from tabItem
		where tabItem.docstatus < 2
			and tabItem.has_variants=0
			and tabItem.disabled=0
			and (tabItem.end_of_life > %(today)s or ifnull(tabItem.end_of_life, '0000-00-00')='0000-00-00')
			and (tabItem.`{key}` LIKE %(txt)s
				or tabItem.item_group LIKE %(txt)s
				or tabItem.item_name LIKE %(txt)s
				or tabItem.barcode LIKE %(txt)s
				{description_cond})
			{fcond} {mcond}
		order by
			if(locate(%(_txt)s, name), locate(%(_txt)s, name), 99999),
			if(locate(%(_txt)s, item_name), locate(%(_txt)s, item_name), 99999),
			idx desc,
			name, item_name
		limit %(start)s, %(page_len)s """.format(
		key=searchfield,
		fcond=get_filters_cond(doctype, filters, conditions).replace('%', '%%'),
		mcond=get_match_cond(doctype).replace('%', '%%'),
		description_cond = description_cond),
		{
			"today": nowdate(),
			"txt": "%%%s%%" % txt,
			"_txt": txt.replace("%", ""),
			"start": start,
			"page_len": page_len
		}, as_dict=as_dict)




