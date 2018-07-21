app_name = "hotel_management"
app_title = "Hotel Management"
app_publisher = "Frappe"
app_description = "App for managing Hotel"
app_icon = "fa fa-bed"
app_color = "#728C00"
app_email = "wachangasteve@gmail.com"
app_url = "http://terester.com"
app_version = "0.0.1"

# role_home_page = {
# 	"Library Member": "article"
# }

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/library_management/css/library_management.css"
# app_include_js = "/assets/library_management/js/library_management.js"

# include js, css files in header of web template
# web_include_css = "/assets/library_management/css/library_management.css"
# web_include_js = "/assets/library_management/js/library_management.js"

# Installation
# ------------

# before_install = "library_management.install.before_install"
# after_install = "library_management.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "library_management.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.core.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.core.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# # }
# doc_events = {
#     "Hotel Room Reservation":{
#         "on_cancel": "hotel_management.hotel_management.doctype.hotel_room_reservation.hotel_room_reservation.release_room"
#     }
# }


# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"daily": [
# 		"library_management.tasks.daily"
# 	],
# }

# scheduler_events = {
# 	"all": [
# 		"library_management.tasks.all"
# 	],
# 	"daily": [
# 		"library_management.tasks.daily"
# 	],
# 	"hourly": [
# 		"library_management.tasks.hourly"
# 	],
# 	"weekly": [
# 		"library_management.tasks.weekly"
# 	]
# 	"monthly": [
# 		"library_management.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "library_management.install.before_tests"

