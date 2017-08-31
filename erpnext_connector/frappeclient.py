# See license

from __future__ import unicode_literals
import frappe, json, requests
from frappe import _
from .account_manager import get_info_via_oauth, get_auth_token, get_auth_headers

@frappe.whitelist()
def bulk_update(docs):
	access_token = get_auth_token(frappe.session.user)
	frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
	headers = get_auth_headers(access_token)
	payload = {
		"docs":docs
	}
	data = requests.post(
		frappe_server_url + "/api/method/frappe.client.bulk_update",
		data=payload,
		headers=headers
	)
	return data.json().get("message")	

@frappe.whitelist()
def cancel(doctype, name):
	access_token = get_auth_token(frappe.session.user)
	frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
	headers = get_auth_headers(access_token)
	payload = {
		"doctype":doctype,
		"name":name
	}
	data = requests.post(
		frappe_server_url + "/api/method/frappe.client.cancel",
		data=payload,
		headers=headers
	)
	return data.json().get("message")	

@frappe.whitelist()
def delete(doctype, name):
	access_token = get_auth_token(frappe.session.user)
	frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
	headers = get_auth_headers(access_token)
	payload = {
		"doctype":doctype,
		"name":name
	}
	data = requests.post(
		frappe_server_url + "/api/method/frappe.client.delete",
		data=payload,
		headers=headers
	)
	return data.json().get("message")

@frappe.whitelist()
def get(doctype, name=None, filters=None):
	access_token = get_auth_token(frappe.session.user)
	frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
	headers = get_auth_headers(access_token)
	payload = {
		"doctype":doctype,
		"name":name,
		"filters": filters
	}
	data = requests.get(
		frappe_server_url + "/api/method/frappe.client.get",
		data=payload,
		headers=headers
	)
	return data.json().get("message")

@frappe.whitelist()
def get_list(doctype, fields=None, filters=None, order_by=None, limit_start=None, limit_page_length=20):
	access_token = get_auth_token(frappe.session.user)
	frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
	headers = get_auth_headers(access_token)
	payload = {
		"doctype":doctype,
		"fields":fields,
		"filters": filters,
		"order_by": order_by,
		"limit_start": limit_start,
		"limit_page_length":limit_page_length
	}
	data = requests.get(
		frappe_server_url + "/api/method/frappe.client.get_list",
		data=payload,
		headers=headers
	)
	return data.json().get("message")

@frappe.whitelist()
def get_value(doctype, fieldname, filters=None, as_dict=True, debug=False):
	access_token = get_auth_token(frappe.session.user)
	frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
	headers = get_auth_headers(access_token)
	payload = {
		"doctype":doctype,
		"fieldname":fieldname,
		"filters": filters,
		"as_dict": as_dict,
		"debug": debug
	}
	data = requests.get(
		frappe_server_url + "/api/method/frappe.client.get_value",
		data=payload,
		headers=headers
	)
	return data.json().get("message")

@frappe.whitelist()
def insert(doc=None):
	access_token = get_auth_token(frappe.session.user)
	frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
	headers = get_auth_headers(access_token)
	payload = {
		"doc":doc
	}
	data = requests.post(
		frappe_server_url + "/api/method/frappe.client.insert",
		data=payload,
		headers=headers
	)
	return data.json().get("message")

@frappe.whitelist()
def insert_many(docs=None):
	access_token = get_auth_token(frappe.session.user)
	frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
	headers = get_auth_headers(access_token)
	payload = {
		"docs":docs
	}
	data = requests.post(
		frappe_server_url + "/api/method/frappe.client.insert_many",
		data=payload,
		headers=headers
	)
	return data.json().get("message")

@frappe.whitelist()
def rename_doc(doctype, old_name, new_name, merge=False):
	access_token = get_auth_token(frappe.session.user)
	frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
	headers = get_auth_headers(access_token)
	payload = {
		"doctype":doctype,
		"old_name":old_name,
		"new_name":new_name,
		"merge":merge
	}
	data = requests.post(
		frappe_server_url + "/api/method/frappe.client.rename_doc",
		data=payload,
		headers=headers
	)
	return data.json().get("message")

@frappe.whitelist()
def set_default(key, value, parent=None):
	access_token = get_auth_token(frappe.session.user)
	frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
	headers = get_auth_headers(access_token)
	payload = {
		"key":key,
		"value":value,
		"parent":parent
	}
	data = requests.post(
		frappe_server_url + "/api/method/frappe.client.set_default",
		data=payload,
		headers=headers
	)
	return data.json().get("message")

@frappe.whitelist()
def set_value(doctype, name, fieldname, value=None):
	access_token = get_auth_token(frappe.session.user)
	frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
	headers = get_auth_headers(access_token)
	payload = {
		"doctype":doctype,
		"name":name,
		"fieldname":fieldname,
		"value":value
	}
	data = requests.post(
		frappe_server_url + "/api/method/frappe.client.set_value",
		data=payload,
		headers=headers
	)
	return data.json().get("message")

@frappe.whitelist()
def submit(doctype, docname):
	access_token = get_auth_token(frappe.session.user)
	frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
	headers = get_auth_headers(access_token)
	payload = {
		"data":"{\"docstatus\":1}"
	}
	data = requests.put(
		frappe_server_url + "/api/resource/" + doctype + "/" + docname,
		data=payload,
		headers=headers
	)
	return data.json().get("data")

@frappe.whitelist()
def add_assign_to(args=None):
	access_token = get_auth_token(frappe.session.user)
	frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
	headers = get_auth_headers(access_token)
	data = requests.post(
		frappe_server_url + "/api/method/frappe.desk.form.assign_to.add",
		data=args,
		headers=headers
	)
	return data.json().get("message")
