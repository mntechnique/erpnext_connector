# see license

from __future__ import unicode_literals
import frappe
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
		error = parse_html(data.text, 'pre')
		print(error)
		return error
