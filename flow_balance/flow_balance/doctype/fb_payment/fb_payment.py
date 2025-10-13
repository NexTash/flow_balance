# Copyright (c) 2025, NexTash (SMC-PVT) Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FBPayment(Document):
	def on_submit(self):
		old_balance = frappe.db.get_value("FB Account", self.account, "balance") or 0
		new_balance = old_balance + self.amount
		frappe.db.set_value("FB Account", self.account, "balance", new_balance) 

	def on_cancel(self):
		old_balance = frappe.db.get_value("FB Account", self.account, "balance") or 0
		new_balance = old_balance - self.amount
		frappe.db.set_value("FB Account", self.account, "balance", new_balance) 
