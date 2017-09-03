# see license
from __future__ import unicode_literals
import frappe, json, requests
from frappe.utils.oauth import get_oauth2_flow, get_oauth2_providers, \
								get_redirect_uri, get_oauth2_authorize_url
from frappe import _

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
	if frappe.db.exists("User", token_user):
		save_token(token_user, token)
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

	bearer_token = get_token_data(user)

	frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
	openid_endpoint = "/api/method/frappe.integrations.oauth2.openid_profile"
	token_endpoint = "/api/method/frappe.integrations.oauth2.get_token"
	# Request for bearer token
	try:
		valid_access_token = bearer_token.get("data").get("access_token")
		auth_headers = get_auth_headers(bearer_token.get("data").get("access_token"))
		openid_response = requests.get(frappe_server_url + openid_endpoint, headers=auth_headers).json()
		return bearer_token.get("data").get("access_token")
	except Exception as e:
		try:
			headers = {'content-type':'application/x-www-form-urlencoded'}
			# Refresh token
			payload = "grant_type=refresh_token&refresh_token="
			payload += bearer_token.get("data").get("refresh_token")
			payload += "&redirect_uri="
			payload += get_redirect_uri("frappe") 
			payload += "&client_id="
			payload += bearer_token.get("data").get("client")
			token_response = requests.post(frappe_server_url + token_endpoint, data=payload, headers=headers).json()
			auth_headers["Authorization"] = "Bearer " + token_response.get("access_token")

			bearer_token = requests.get(
				frappe_server_url + "/api/resource/OAuth%20Bearer%20Token/" + token_response.get("access_token"),
				data={"fields":'["*"]'},
				headers=auth_headers
			).json()

			save_token(token_user=bearer_token.get('data').get("user"), token=bearer_token)
			revoke_token(valid_access_token)
			return bearer_token.get("data").get("access_token")
		except Exception as e:
			respond_error()

def respond_error():
	auth_url = get_oauth2_authorize_url('frappe')
	frappe.throw(_('<a href="' + auth_url + '" class="btn btn-primary">login via Frappe</a>'), title=_("Session Expired"))

def revoke_token(valid_access_token=None):
	if valid_access_token:
		frappe_server_url = frappe.db.get_value("Social Login Keys", None, "frappe_server_url")
		revoke_token_endpoint = "/api/method/frappe.integrations.oauth2.revoke_token"
		payload = {'token':valid_access_token}
		requests.post(
			frappe_server_url + revoke_token_endpoint,
			data=payload
		)

def save_token(token_user, token):
	save_token_in = frappe.get_doc("ERPNext Connector Settings").get("save_token_in")
	if save_token_in == "DocType":
		try:
			connector_user_data = frappe.get_doc("Connector User Data", token_user)
		except Exception as e:
			connector_user_data = frappe.new_doc("Connector User Data")
		connector_user_data.user = token_user
		connector_user_data.bearer_token = json.dumps(token)
		connector_user_data.save(ignore_permissions=True)
		frappe.db.commit()
	elif save_token_in == "Redis":
		key = token_user + "_bearer_token"
		rs = frappe.cache()
		rs.set_value(key, json.dumps(token))

def get_token_data(user):
	save_token_in = frappe.get_doc("ERPNext Connector Settings").get("save_token_in")
	try:
		if save_token_in == "DocType":
			token_code = frappe.db.get_value("Connector User Data", user, "bearer_token")
			bearer_token = json.loads(token_code)
			return bearer_token
		elif save_token_in == "Redis":
			rs = frappe.cache()
			bearer_token = json.loads(rs.get_value("{0}_bearer_token".format(user)))
			return bearer_token
	except Exception as e:
		return None

def get_auth_headers(token):
	auth_headers = {
		'content-type':'application/x-www-form-urlencoded',
		'Authorization':'Bearer ' + token
	}
	return auth_headers