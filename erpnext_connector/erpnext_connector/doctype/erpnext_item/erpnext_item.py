# -*- coding: utf-8 -*-
# Copyright (c) 2017, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, requests
import erpnext_connector
from frappe.model.document import Document

class ERPNextItem(Document):
	pass

def erpnext_item_query(doctype, txt, searchfield, start, page_len, filters):
	data = get_items()
	out = []
	for d in data:
		out.append(tuple([d.get("name"),d.get("item_name")]))
	out = [o for o in out if (txt.lower() in o[0].lower()) or (txt.lower() in o[1].lower())]
	return out

def get_items():
	data = erpnext_connector.get_all(doctype="Item")
	local_data = frappe.get_all("ERPNext Item")
	for d in data:
		if not d.get("name") in [l.get("name") for l in local_data]:
			erpnext_item = frappe.new_doc("ERPNext Item")
			erpnext_item.item_name = d.get('name')
			erpnext_item.save(ignore_permissions=True)
			frappe.db.commit()

	return data