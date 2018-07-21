// Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Hotel Room Reservation', {
    setup: function(frm) {
    		let get_item_query = () => {
    			return {
    				query: 'hotel_management.hotel_management.doctype.hotel_room_reservation.hotel_room_reservation.item_query_room',
    				filters: {
    					'hotel_room': frm.doc.hotel_room
    				}
    			};
    		};
    //	    item is a field in table items
    		frm.set_query('item', 'items', get_item_query);
//    		frm.set_query('add_item', get_item_query);
    	},
	refresh: function(frm) {
		if(frm.doc.docstatus == 1){
			frm.add_custom_button(__("Make Invoice"), ()=> {
				frm.trigger("make_invoice");
			});
            frm.add_custom_button(__("Release Room"), ()=> {
                frm.trigger("release_room");
            });
		}
		else{
		 frm.add_custom_button(__("Check Rooms Available"), ()=> {
              frm.trigger("nav_room");
              });
		}
        frm.set_query('hotel_room', function () {
            return {
                filters: [
                    ['Hotel Room', 'status', '=', 'Available']
                ]
            }
            frm.refresh();
        });

	},
	from_date: function(frm) {
		frm.trigger("recalculate_rates");
	},
	to_date: function(frm) {
		frm.trigger("recalculate_rates");
	},
	recalculate_rates: function(frm) {
		if (!frm.doc.from_date || !frm.doc.to_date
			|| !frm.doc.items.length){
			return;
		}
		frappe.call({
			"method": "hotel_management.hotel_management.doctype.hotel_room_reservation.hotel_room_reservation.get_room_rate",
			"args": {"hotel_room_reservation": frm.doc}
		}).done((r)=> {
			for (var i = 0; i < r.message.items.length; i++) {
				frm.doc.items[i].rate = r.message.items[i].rate;
				frm.doc.items[i].amount = r.message.items[i].amount;
			}
			frappe.run_serially([
				()=> frm.set_value("net_total", r.message.net_total),
				()=> frm.refresh_field("items")
			]);
		});
	},
	make_invoice: function(frm) {
		frappe.model.with_doc("Hotel Settings", "Hotel Settings", ()=>{
			frappe.model.with_doctype("Sales Invoice", ()=>{
				let hotel_settings = frappe.get_doc("Hotel Settings", "Hotel Settings");
				let invoice = frappe.model.get_new_doc("Sales Invoice");
				invoice.customer = frm.doc.customer || hotel_settings.default_customer;
				if (hotel_settings.default_invoice_naming_series){
					invoice.naming_series = hotel_settings.default_invoice_naming_series;
				}
				for (let d of frm.doc.items){
					let invoice_item = frappe.model.add_child(invoice, "items")
					invoice_item.item_code = d.item;
					invoice_item.qty = d.qty;
					invoice_item.rate = d.rate;
					invoice_item.item_name = d.item;
					invoice_item.description = d.item;
					invoice_item.uom = "Nos";
					invoice_item.income_account = "Sales - BCL";
				}
				if (hotel_settings.default_taxes_and_charges){
					invoice.taxes_and_charges = hotel_settings.default_taxes_and_charges;
				}
				frappe.set_route("Form", invoice.doctype, invoice.name);
			});
		});
	},
	nav_room: function(){
	    frappe.route_options = {
	        "status" : "Available"
	    };
	    frappe.set_route("List", "Hotel Room");
	},
	release_room: function(frm) {
	     frappe.call({
	            "method" : "hotel_management.hotel_management.doctype.hotel_room_reservation.hotel_room_reservation.release_room",
	            "args" : {"hotel_room" : frm.doc.hotel_room}
	     });
	}
});


frappe.ui.form.on('Hotel Room Reservation Item', {
	item: function(frm, doctype, name) {
		frm.trigger("recalculate_rates");
	},
	qty: function(frm) {
		frm.trigger("recalculate_rates");
	}
});
