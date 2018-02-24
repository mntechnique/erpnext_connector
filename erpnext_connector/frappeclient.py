# See license

from __future__ import unicode_literals
import frappe, json, requests
from frappe import _
from frappe.frappeclient import FrappeClient
from .account_manager import get_info_via_oauth, get_auth_token, get_auth_headers
from .utils import parse_data

@frappe.whitelist()
def bulk_update(docs, get_response=False):
	access_token = get_auth_token(frappe.session.user)
	frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
	headers = get_auth_headers(access_token)
	payload = {
		"docs":json.dumps(docs)
	}
	data = requests.post(
		frappe_server_url + "/api/method/frappe.client.bulk_update",
		data=payload,
		headers=headers
	)
	return parse_data(data, get_response)

@frappe.whitelist()
def cancel(doctype, name, get_response=False):
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
	return parse_data(data, get_response)

@frappe.whitelist()
def delete(doctype, name, get_response=False):
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
	return parse_data(data, get_response)

@frappe.whitelist()
def get(doctype, name=None, filters=None, get_response=False):
	access_token = get_auth_token(frappe.session.user)
	frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
	headers = get_auth_headers(access_token)
	payload = {
		"doctype":doctype
	}
	if name: payload["name"] = name
	if filters: payload["filters"] = json.dumps(filters)
	payload = '&'.join(["{}={}".format(k, v) for k, v in payload.items()])
	data = requests.get(
		frappe_server_url + "/api/method/frappe.client.get",
		data=payload,
		headers=headers
	)
	return parse_data(data, get_response)

@frappe.whitelist()
def get_list(doctype, fields=None, filters=None, order_by=None,
				limit_start=None, limit_page_length=20, get_response=False):
	access_token = get_auth_token(frappe.session.user)
	frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
	headers = get_auth_headers(access_token)
	payload = {
		"doctype":doctype,
		"limit_page_length":limit_page_length
	}
	if fields: payload["fields"] = json.dumps(fields)
	if filters: payload["filters"] = json.dumps(filters)
	if order_by: payload["order_by"] = order_by
	if limit_start: payload["limit_start"] = limit_start
	payload = '&'.join(["{}={}".format(k, v) for k, v in payload.items()])
	data = requests.get(
		frappe_server_url + "/api/method/frappe.client.get_list",
		data=payload,
		headers=headers
	)
	return parse_data(data, get_response)

@frappe.whitelist()
def get_value(doctype, fieldname, filters=None, as_dict=True, debug=False, get_response=False):
	access_token = get_auth_token(frappe.session.user)
	frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
	headers = get_auth_headers(access_token)
	payload = {
		"doctype":doctype,
		"fieldname":fieldname
	}
	if filters: payload["filters"] = json.dumps(filters)
	if as_dict: payload["as_dict"] = as_dict
	if debug: payload["debug"] = debug
	payload = '&'.join(["{}={}".format(k, v) for k, v in payload.items()])
	data = requests.get(
		frappe_server_url + "/api/method/frappe.client.get_value",
		data=payload,
		headers=headers
	)
	return parse_data(data, get_response)

@frappe.whitelist()
def insert(doc=None, get_response=False):
	access_token = get_auth_token(frappe.session.user)
	frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
	headers = get_auth_headers(access_token)
	payload = {}
	if doc: payload["doc"] = json.dumps(doc)
	data = requests.post(
		frappe_server_url + "/api/method/frappe.client.insert",
		data=payload,
		headers=headers
	)
	return data.json().get("message") if not get_response else data

@frappe.whitelist()
def insert_many(docs=None, get_response=False):
	access_token = get_auth_token(frappe.session.user)
	frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
	headers = get_auth_headers(access_token)
	payload = {}
	if docs: payload["docs"] = json.dumps(docs)
	data = requests.post(
		frappe_server_url + "/api/method/frappe.client.insert_many",
		data=payload,
		headers=headers
	)
	return parse_data(data, get_response)

@frappe.whitelist()
def rename_doc(doctype, old_name, new_name, merge=False, get_response=False):
	access_token = get_auth_token(frappe.session.user)
	frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
	headers = get_auth_headers(access_token)
	payload = {
		"doctype":doctype,
		"old_name":old_name,
		"new_name":new_name,
	}
	if merge: payload["merge"] = merge
	data = requests.post(
		frappe_server_url + "/api/method/frappe.client.rename_doc",
		data=payload,
		headers=headers
	)
	return parse_data(data, get_response)

@frappe.whitelist()
def set_default(key, value, parent=None, get_response=False):
	access_token = get_auth_token(frappe.session.user)
	frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
	headers = get_auth_headers(access_token)
	payload = {
		"key":key,
		"value":value,
	}
	if parent: payload["parent"] = parent
	data = requests.post(
		frappe_server_url + "/api/method/frappe.client.set_default",
		data=payload,
		headers=headers
	)
	return parse_data(data, get_response)

@frappe.whitelist()
def set_value(doctype, name, fieldname, value=None, get_response=False):
	access_token = get_auth_token(frappe.session.user)
	frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
	headers = get_auth_headers(access_token)
	payload = {
		"doctype":doctype,
		"name":name,
		"fieldname":fieldname
	}
	if value: payload["value"] = value
	data = requests.post(
		frappe_server_url + "/api/method/frappe.client.set_value",
		data=payload,
		headers=headers
	)
	return parse_data(data, get_response)

@frappe.whitelist()
def submit(doctype, docname, get_response=False):
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
	return parse_data(data, get_response, key='data')

@frappe.whitelist()
def add_assign_to(args=None, get_response=False):
	access_token = get_auth_token(frappe.session.user)
	frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
	headers = get_auth_headers(access_token)
	data = requests.post(
		frappe_server_url + "/api/method/frappe.desk.form.assign_to.add",
		data=args,
		headers=headers
	)
	return parse_data(data, get_response)

class FrappeOAuth2Client(FrappeClient):
	def __init__(self, url, access_token, verify=True):
		self.access_token = access_token
		self.headers = {
			"Authorization": "Bearer " + access_token,
			"content-type": "application/x-www-form-urlencoded"
		}
		self.verify = verify
		self.session = OAuth2Session(self.headers)
		self.url = url

	def get_request(self, params):
		res = requests.get(self.url, params=self.preprocess(params), headers=self.headers, verify=self.verify)
		res = self.post_process(res)
		return res

	def post_request(self, data):
		res = requests.post(self.url, data=self.preprocess(data), headers=self.headers, verify=self.verify)
		res = self.post_process(res)
		return res

class OAuth2Session():
	def __init__(self, headers):
		self.headers = headers
	def get(self, url, params, headers, verify):
		res = requests.get(url, params=params, headers=self.headers, verify=verify)
		return res
	def post(self, url, data, headers, verify):
		res = requests.post(url, data=data, headers=self.headers, verify=verify)
		return res
	def put(self, url, data, verify):
		res = requests.put(url, data=data, headers=self.headers, verify=verify)
		return res
