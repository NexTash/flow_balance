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
