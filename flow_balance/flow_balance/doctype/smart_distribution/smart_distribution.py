# Copyright (c) 2025, NexTash (SMC-PVT) Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SmartDistribution(Document):
	@frappe.whitelist()
	def get_distribution(self):
		# get available balance from FB Account
		available_balance = frappe.db.get_value("FB Account", self.account, "balance")
		
		# find employees where the last clearance date is not in this month
		employees = frappe.get_all(
			"FB Employee",
			filters={
				"last_clearance_date": ["<",frappe.utils.get_first_day(frappe.utils.nowdate())],
			},
			fields=["name", "full_name", "cts_threshold_amount", "cts_threshold_date"],
			order_by="cts_threshold_date asc",
		)
		
		if not employees:
			frappe.msgprint("No employees found for distribution.")
			return "No employees found for distribution."

		
		self.set("distribution", [])
		for row in employees:
			if available_balance <= 0:
				break

			if available_balance <= row.cts_threshold_amount:
				amount = available_balance
			else:
				amount = row.cts_threshold_amount

			available_balance -= amount

			self.append(
				"distribution",
				{	
					"employee": row.name,
					"amount": amount,
				},
			)
		
		self.save()

		return "Distribution details updated."
