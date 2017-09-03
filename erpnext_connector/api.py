# See license

from __future__ import unicode_literals
import frappe, json, requests
from frappe.utils.oauth import login_oauth_user
from .frappeclient import get_list
from frappe import _

from .account_manager import get_info_via_oauth, get_auth_token, get_auth_headers

@frappe.whitelist(allow_guest=True)
def login_via_frappe(code, state):
	info = get_info_via_oauth("frappe", code, json.loads)
	login_oauth_user(info, provider="frappe", state=state)

def upstream_doc_query(doctype, txt, searchfield, start, page_len, filters):
	hooks = frappe.get_hooks()
	upstream_doctype = doctype.split("ERPNext ")[1]
	if hooks.get("erpnext_connector_search_fields") and hooks.get("erpnext_connector_search_fields").get(upstream_doctype):
		searchfield = hooks.get("erpnext_connector_search_fields").get(upstream_doctype)
	remote_data = get_upstream_docs(upstream_doctype, searchfield, page_len, filters)
	compare_data = []
	out = []
	for d in remote_data:
		if type(searchfield) == list:
			compare_data.append(tuple(d.get(f) for f in searchfield if d.get(f)))
		else:
			compare_data.append(tuple([d.get(searchfield)]))
	out = [ti for ti in compare_data if len([st for st in ti if txt.lower() in st.lower()]) > 0]
	return out

def get_upstream_docs(doctype, fields, page_len, filters):

	if fields == 'name':
		fields = ["name"]
	if type(filters) == list:
		for i in filters:
			fields.append(i[0])
	elif type(filters) == dict:
		fields = filters.keys()
		fields.append("name")

	connector_doctype = "ERPNext " + doctype

	data = get_list(doctype=doctype, fields=fields, filters=filters, limit_page_length=page_len)
	local_data = frappe.get_all(connector_doctype)
	for d in data:
		if not d.get("name") in [l.get("name") for l in local_data]:
			doc = frappe.new_doc(connector_doctype)
			doc[ frappe.scrub(doctype) + '_name'] = d.get('name')
			doc.save(ignore_permissions=True)
			frappe.db.commit()
	return data
