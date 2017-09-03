# -*- coding: utf-8 -*-
# Copyright (c) 2017, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, requests
from frappe.model.document import Document
from erpnext_connector.api import upstream_doc_query
import erpnext_connector

class ERPNextCompany(Document):
	pass

