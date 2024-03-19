# Copyright (c) 2024, John Vincent Fiel and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from erpnext.patches.v14_0.migrate_gl_to_payment_ledger import execute
class HCDCSettings(Document):
	@frappe.whitelist()
	def refresh_payment_ledger(self):
		frappe.db.sql(""" TRUNCATE `tabPayment Ledger Entry` """)
		frappe.db.commit()
		execute()
		frappe.msgprint("Completed")


	
