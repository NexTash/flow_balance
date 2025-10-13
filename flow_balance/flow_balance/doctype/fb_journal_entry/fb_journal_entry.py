# Copyright (c) 2025, NexTash (SMC-PVT) Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe import _ 
from frappe.model.document import Document


class FBJournalEntry(Document):
	def validate(self):
		for row in self.jv_details:
			if (not row.get("debit", 0) or row.get("debit", 0) < 1) and (not row.get("credit", 0) or row.get("credit", 0) < 1):
				frappe.throw(_("Each row shall have atleast one balance positive (credit/debit)"))
		
	
	def on_submit(self):
		for row in self.jv_details:
			if row.get("debit", 0) and row.get("debit", 0) > 0:
				old_balance = frappe.db.get_value("FB Account", row.account, "balance") or 0
				new_balance = old_balance + row.debit
				frappe.db.set_value("FB Account", row.account, "balance", new_balance)

				employee = row.get("against_employee")
				frappe.db.set_value("FB Employee", employee, "last_clearance_date", self.posting_date)

			if row.get("credit", 0) and row.get("credit", 0) > 0:
				old_balance = frappe.db.get_value("FB Account", row.account, "balance") or 0
				new_balance = old_balance - row.credit
				frappe.db.set_value("FB Account", row.account, "balance", new_balance)
