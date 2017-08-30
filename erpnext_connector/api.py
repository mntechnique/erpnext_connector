# See license

from __future__ import unicode_literals
import frappe, json, requests
from frappe.utils.oauth import login_oauth_user, get_oauth2_flow, get_oauth2_providers, \
								get_redirect_uri, get_oauth2_authorize_url
from frappe import _

@frappe.whitelist(allow_guest=True)
def login_via_frappe(code, state):
	info = get_info_via_oauth("frappe", code, json.loads)
	login_oauth_user(info, provider="frappe", state=state)

def get_info_via_oauth(provider, code, decoder=None):
	flow = get_oauth2_flow(provider)
	oauth2_providers = get_oauth2_providers()

	args = {
		"data": {
			"code": code,
			"redirect_uri": get_redirect_uri(provider),
			"grant_type": "authorization_code"
		}
	}

	if decoder:
		args["decoder"] = decoder

	session = flow.get_auth_session(**args)

	token_response = session.get("/api/resource/OAuth%20Bearer%20Token/" + session.access_token, 
		params={"fields":'["*"]'})
	token = token_response.json()
	token_user = token.get("data").get("user")
	key = token_user + "_bearer_token"
	rs = frappe.cache()
	rs.set_value(key, json.dumps(token))

	api_endpoint = oauth2_providers[provider].get("api_endpoint")
	api_endpoint_args = oauth2_providers[provider].get("api_endpoint_args")
	info = session.get(api_endpoint, params=api_endpoint_args).json()

	if (("verified_email" in info and not info.get("verified_email"))
		or ("verified" in info and not info.get("verified"))):
		frappe.throw(_("Email not verified with {1}").format(provider.title()))

	return info

def get_auth_token(user=None):
	if not user:
		user = frappe.session.user

	rs = frappe.cache()
	try:
		bearer_token = json.loads(rs.get_value("{0}_bearer_token".format(user)))
	except Exception as e:
		respond_error()

	auth_headers = {
		'content-type':'application/x-www-form-urlencoded',
		'Authorization':'Bearer ' + bearer_token.get("data").get("access_token")
	}
	frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
	openid_endpoint = "/api/method/frappe.integrations.oauth2.openid_profile"
	token_endpoint = "/api/method/frappe.integrations.oauth2.get_token"
	# Request for bearer token
	try:
		openid_response = requests.get(frappe_server_url + openid_endpoint, headers=auth_headers).json()
		return bearer_token.get("data").get("access_token")
	except Exception as e:
		headers = {'content-type':'application/x-www-form-urlencoded'}
		# Refresh token
		payload = "grant_type=refresh_token&refresh_token="
		payload += bearer_token.get("data").get("refresh_token")
		payload += "&redirect_uri="
		payload += get_redirect_uri("frappe") 
		payload += "&client_id="
		payload += bearer_token.get("data").get("client")

		try:
			token_response = requests.post(frappe_server_url + token_endpoint, data=payload, headers=headers).json()
			auth_headers["Authorization"] = "Bearer " + token_response.get("access_token")

			bearer_token = requests.get(
				frappe_server_url + "/api/resource/OAuth%20Bearer%20Token/" + token_response.get("access_token"),
				data={"fields":'["*"]'},
				headers=auth_headers
			).json()

			key = bearer_token.get('data').get("user") + "_bearer_token"
			rs = frappe.cache()
			rs.set_value(key, json.dumps(bearer_token))
			return bearer_token.get("data").get("access_token")
		except Exception as e:
			respond_error()

@frappe.whitelist()
def get_all(doctype=None):
	if not doctype:
		frappe.throw(_("DocType not found"))
	access_token = get_auth_token(frappe.session.user)
	frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
	payload = 'fields=["*"]&'
	payload += 'limit_page_length=None'
	headers = {
		'content-type':'application/x-www-form-urlencoded',
		'Authorization': 'Bearer ' + access_token
	}

	data = requests.get(
		frappe_server_url + "/api/resource/" + doctype,
		data=payload,
		headers=headers
	)
	return data.json().get("data")

@frappe.whitelist()
def get_doc(doctype=None, docname=None):
	if not doctype:
		frappe.throw(_("DocType not found"))
	if not docname:
		frappe.throw(_("Docname not found"))
	access_token = get_auth_token(frappe.session.user)
	frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
	headers = {
		'content-type':'application/x-www-form-urlencoded',
		'Authorization': 'Bearer ' + access_token
	}

	data = requests.get(
		frappe_server_url + "/api/resource/" + doctype + "/" + docname,
		headers=headers
	)
	return data.json().get("data")

def respond_error():
	auth_url = get_oauth2_authorize_url('frappe')
	frappe.throw(_('<a href="' + auth_url + '" class="btn btn-primary">login via Frappe</a>'), title=_("Session Expired"))