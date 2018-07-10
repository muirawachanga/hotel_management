// Copyright (c) 2016, Bituls Company Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */
frappe.query_reports["Hotel Room Occupancy"] = {
		"filters": [
    		{
    			"fieldname":"from_date",
    			"label": __("From Date"),
    			"fieldtype": "Datetime",
    			"default": frappe.datetime.get_today(),
    			"width": "80"
    		},
    		{
    			"fieldname":"to_date",
    			"label": __("To Date"),
    			"fieldtype": "Datetime",
    			"default": frappe.datetime.now_datetime()
    		},
    		{
    			"fieldname":"customer",
    			"label": __("Customer"),
    			"fieldtype": "Link",
    			"options": "Customer"
    		}

	]
}
