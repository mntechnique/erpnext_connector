# See license

from __future__ import unicode_literals
import frappe, json, requests
from frappe.utils.oauth import login_oauth_user
from .frappeclient import get_list
from .account_manager import respond_error
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
	try:
		remote_data = get_upstream_docs(upstream_doctype, searchfield, page_len, filters)
	except Exception as e:
		remote_data = None
		respond_error()
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
			setattr(doc, frappe.scrub(doctype) + '_name', d.get('name'))
			doc.save(ignore_permissions=True)
			frappe.db.commit()
	return data

def get_token_page():
	javascript = """$(() => {
		const route = localStorage.getItem("microservice_route");
		if (route) {
			const go_to = window.location.origin
			+ route + "?access_token="
			+ get_parameter_by_name("access_token");
			window.location.href = go_to;
		}
	});

	get_parameter_by_name(name) => {
		name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
		let regex = new RegExp("[\\#&]" + name + "=([^&#]*)"),
		results = regex.exec(location.hash);
		return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
	}
	"""
	token_page =  {
		"doctype": "Web Page",
		"insert_code" : 1,
		"insert_style" : 0,
		"javascript": javascript,
		"main_section" : "<div style=\"text-align: center;\">Authorizing ...</div>",
		"name" : "token",
		"published" : 1,
		"route" : "token",
		"show_sidebar" : 0,
		"show_title": 0,
		"title": "token"
	}

def get_custom_script():
	custom_script = """
		authorize(server_url, client_id, redirect_uri) => {
			console.log("Authorizing...");

			// queryStringData is details of OAuth Client (Implicit Grant) on Custom App
			let queryStringData = {
				response_type : "token",
				client_id : client_id,
				redirect_uri : redirect_uri
			}

			// Clear previously set microservice_route if any
			localStorage.removeItem("microservice_route");

			// Get current raw route and build url
			const route = "/desk#" + frappe.get_raw_route_str();

			// Set route in localStorage
			localStorage.setItem("microservice_route", route);

			// Go authorize!
			window.location.replace(server_url + "/api/method/frappe.integrations.oauth2.authorize?" + jQuery.param(queryStringData));
		}

		consume_token(endpoint, data, method) => {
			const token = frappe.urllib.get_arg("access_token");
			const route = localStorage.getItem("microservice_route");

			// if page has route with parameter ?access_token=420 and microservice_route is in localStorage.
			if (token && route) {

				// Clean up access token from route
				frappe.set_route(frappe.get_route().join("/"))

				// query protected resource e.g. openid_profile with token
				let call = {
					"async": true,
					"crossDomain": true,
					"url": endpoint,
					"method": method || "GET",
					"data": {
						"data": JSON.stringify(data)
					},
					"headers": {
						"authorization": "Bearer " + token,
						"content-type": "application/x-www-form-urlencoded"
					}
				}

				$.ajax(call).done(function (response) {
					// display response
					console.log(response);

					frappe.show_alert(response)

					// clear microservice_route from localStorage
					localStorage.removeItem("microservice_route");
				});
			}
		}
	"""
	return custom_script
