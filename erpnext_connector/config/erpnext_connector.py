# see license
from frappe import _

def get_data():
	return [
		{
			"label": _("Setup"),
			"icon": "icon-settings",
			"items": [
				{
					"type": "doctype",
					"name": "ERPNext Connector Settings",
					"label": "ERPNext Connector Settings",
					"description": _("ERPNext Connector Settings")
				}
			]
		}
	]
