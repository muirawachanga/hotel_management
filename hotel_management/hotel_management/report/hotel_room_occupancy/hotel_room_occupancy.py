# Copyright (c) 2013, Bituls Company Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _

def execute(filters=None):
	return _execute(filters)


def get_conditions(filters):
	if filters.get("to_date") < filters.get("from_date"):
		msgprint(_("Please sent date accordingly"))
	conditions = ""
	# if filters.get("no_of_people"): conditions += " and no_of_people=%(no_of_people)s"
	# if filters.get("reservation_instructions"): conditions += " and reservation_instructions = %(reservation_instructions)s"

	if filters.get("from_date"): conditions += " and creation>=%(from_date)s"
	if filters.get("to_date"): conditions += " and creation<=%(to_date)s"

	if filters.get("customer"): conditions += " and customer = %(customer)s"

	return conditions

def _execute(filters):
	if not filters: filters = frappe._dict({})
	data = []
	columns = get_columns()
	reservation_list = get_reservation(filters)
	# msgprint(_(reservation_list))
	if not reservation_list:
		msgprint(_("No record found"))
		return columns, reservation_list
	extra_it_rate_map = get_extra_it_rate_map(reservation_list)
	for res in reservation_list:
		# msgprint(_(res.name))
		item = list(set(extra_it_rate_map.get(res.name, {}).get("item", [])))
		# rate = list(set(extra_it_rate_map.get(res.name, {}).get("rate", [])))
		row = [res.get("name"), res.get("customer"), res.get("guest_name"),
			   res.get("from_date"), res.get("to_date"),res.get("hotel_room"),
			   res.get("reservation_note")]

		row +=[ ", ".join(item)]
		data.append(row)
	return columns, data

def get_reservation(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""
		select name, customer, guest_name, from_date, to_date, hotel_room, 
		reservation_note
		from `tabHotel Room Reservation` 
		where docstatus = 1 %s order by creation desc""" % conditions, filters, as_dict=1)

def get_columns():
	"""return columns based on filters"""
	columns =[
		_("Name") + ":Link/Hotel Room Reservation:80", _("Customer") + ":Link/Customer:120",
		_("Guest Name") + "::120", _("From Date") + "::120", _("To Date") + "::120",
		_("Hotel Room") + ":Link/Hotel Room:120", _("Package") + "::180",  _("Reservation Note ") + ":Long Text:180"
	]
	return columns

def get_extra_it_rate_map(reservation_list):
	# msgprint(_(reservation_list))
	si_items = frappe.db.sql("""select parent, item
		from `tabHotel Room Reservation Item` where parent in (%s)
		and (ifnull(item, '') != '')""" %
							 ', '.join(['%s']*len(reservation_list)), tuple([res.name for res in reservation_list]), as_dict=1)

	extra_it_rate_map = {}
	for d in si_items:
		if d.item:
			extra_it_rate_map.setdefault(d.parent, frappe._dict()).setdefault(
				"item", []).append(d.item)
	# msgprint(_(extra_it_rate_map))
	return extra_it_rate_map
