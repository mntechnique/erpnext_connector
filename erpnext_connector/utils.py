# see license

from __future__ import unicode_literals
import frappe, requests
from frappe import _

try: 
	from BeautifulSoup import BeautifulSoup
except ImportError:
	from bs4 import BeautifulSoup

def parse_html(html, tag=None):
	parsed_html = BeautifulSoup(html, "lxml")
	return parsed_html if not tag else parsed_html.find(tag).text

def parse_data(data, get_response, key="message"):
	try:
		return data.json().get(key) if not get_response else data
	except Exception as e:
		error = parse_html(data.text, tag='pre')
		print(error)
		return error

def get_timezone(frappe_server_url):
	timezone = requests.get(frappe_server_url + "/api/method/frappe.client.get_time_zone").json().get("message").get("time_zone")
	return timezone
