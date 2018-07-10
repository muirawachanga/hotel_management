from __future__ import unicode_literals

from frappe import _


def get_data():
    return [
        {
            "label": _("Documents"),
            "icon": "icon-star",
            "items": [
                {
                    "type": "doctype",
                    "name": "Hotel Room",
                    "description": _("Create Room")
                },
                {
                    "type": "doctype",
                    "name": "Hotel Room Package",
                    "description": _("Create Package")
                }
            ]
        },
        {
            "label": _("Setup"),
            "icon": "icon-cog",
            "items": [

                {
                    "type": "doctype",
                    "name": "Hotel Room Pricing",
                    "description": _("Create Price.")
                },
                {
                    "type": "doctype",
                    "name": "Hotel Room Pricing Package",
                    "description": _("Create package.")
                },
                {
                    "type": "doctype",
                    "name": "Hotel Room Reservation",
                    "description": _("Create reservations.")
                },
                {
                    "type": "doctype",
                    "name": "Hotel Room Type",
                    "description": _("Create room type.")
                },
                {
                    "type": "doctype",
                    "name": "Hotel Settings",
                    "description": _("Create setting.")
                }
            ]
        },
        {
            "label": _("Standard Reports"),
            "icon": "icon-list",
            "items": [
                {
                    "type": "report",
                    "name": "Hotel Room Occupancy",
                    "is_query_report": True,
                    "doctype": "Hotel Room Reservation"
                }
            ]
        },
        {
            "label": _("Help"),
            "icon": "icon-facetime-video",
            "items": [

            ]
        }
    ]
