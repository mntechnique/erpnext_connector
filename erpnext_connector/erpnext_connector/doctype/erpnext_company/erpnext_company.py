# -*- coding: utf-8 -*-
# Copyright (c) 2017, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, requests
from frappe.model.document import Document
import erpnext_connector

class ERPNextCompany(Document):
	pass

def erpnext_company_query(doctype, txt, searchfield, start, page_len, filters):
	data = get_companies()
	out = []
	for d in data:
		out.append(tuple([d.get("name"),d.get("abbr")]))
	out = [o for o in out if (txt.lower() in o[0].lower()) or (txt.lower() in o[1].lower())]
	return out

def get_companies():
	data = erpnext_connector.get_all(doctype="Company")
	local_data = frappe.get_all("ERPNext Company")
	for d in data:
		if not d.get("name") in [l.get("name") for l in local_data]:
			erpnext_company = frappe.new_doc("ERPNext Company")
			erpnext_company.company_name = d.get('name')
			erpnext_company.save(ignore_permissions=True)
			frappe.db.commit()

	return data
