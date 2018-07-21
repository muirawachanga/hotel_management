frappe.listview_settings['Hotel Room'] = {
    get_indicator: function (doc) {
		return [__(doc.status), {
			"Booked": "orange",
			"Available": "blue"
		}[doc.status], "status,=," + doc.status];
    }
}