# -*- coding: utf-8 -*-
# Copyright (c) 2017, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, requests
import erpnext_connector
from frappe.model.document import Document

class ERPNextPriceList(Document):
	pass

def erpnext_price_list_query(doctype, txt, searchfield, start, page_len, filters):
	data = get_price_list()
	out = []
	for d in data:
		out.append(tuple([d.get("name")]))
	out = [o for o in out if (txt.lower() in o[0].lower())]
	return out

def get_price_list():
	data = erpnext_connector.get_all(doctype="Price List")
	local_data = frappe.get_all("ERPNext Price List")
	for d in data:
		if not d.get("name") in [l.get("name") for l in local_data]:
			erpnext_price_list = frappe.new_doc("ERPNext Price List")
			erpnext_price_list.price_list_name = d.get('name')
			erpnext_price_list.save(ignore_permissions=True)
			frappe.db.commit()

	return data