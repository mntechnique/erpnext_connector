# See license

from __future__ import unicode_literals
import frappe, json, requests
from frappe.utils.oauth import login_oauth_user
from frappe import _

from .account_manager import get_info_via_oauth, get_auth_token, get_auth_headers

@frappe.whitelist(allow_guest=True)
def login_via_frappe(code, state):
	info = get_info_via_oauth("frappe", code, json.loads)
	login_oauth_user(info, provider="frappe", state=state)

@frappe.whitelist()
def get_all(doctype, fields=["*"], filters={}, page_len=None):
	access_token = get_auth_token(frappe.session.user)
	frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
	payload = 'fields=' + json.dumps(fields) + '&'
	payload += 'filters=' + json.dumps(filters) + '&'
	payload += 'limit_page_length=None' if not page_len else 'limit_page_length=' + str(page_len)
	headers = get_auth_headers(access_token)

	data = requests.get(
		frappe_server_url + "/api/resource/" + doctype,
		data=payload,
		headers=headers
	)
	return data.json().get("data")

@frappe.whitelist()
def get_doc(doctype, docname):
	access_token = get_auth_token(frappe.session.user)
	frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
	headers = get_auth_headers(access_token)

	data = requests.get(
		frappe_server_url + "/api/resource/" + doctype + "/" + docname,
		headers=headers
	)
	return data.json().get("data")

def upstream_doc_query(doctype, txt, searchfield, start, page_len, filters):
	remote_data = get_upstream_docs(doctype.split("ERPNext ")[1], searchfield, page_len, filters)
	compare_data = []
	out = []

	for d in remote_data:
		if type(searchfield) == list:
			compare_data.append(tuple([d.get(f) for f in searchfield]))
		else:
			compare_data.append(tuple([d.get(searchfield)]))

	out = [ti for ti in compare_data if len([st for st in ti if txt.lower() in st.lower()]) > 0]
	return out

def get_upstream_docs(doctype, fields, page_len, filters):
	connector_doctype = "ERPNext " + doctype
	data = get_all(doctype=doctype, fields=fields)
	local_data = frappe.get_all(connector_doctype)
	for d in data:
		if not d.get("name") in [l.get("name") for l in local_data]:
			doc = frappe.new_doc(connector_doctype)
			doc[ frappe.scrub(doctype) + '_name'] = d.get('name')
			doc.save(ignore_permissions=True)
			frappe.db.commit()
	local_data = frappe.get_all(connector_doctype)
	return data
