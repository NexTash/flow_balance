// Copyright (c) 2025, NexTash (SMC-PVT) Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on("Smart Distribution", {
	refresh(frm) {
		frm.add_custom_button(__("Get Distribution"), function () {
			frm.call("get_distribution").then(() => {
				frm.reload_doc();
			});
		});

		frm.add_custom_button(__("Make Journal Entry"), function () {
			frappe.model.with_doctype("FB Journal Entry", () => {
				// route to adjustment Journal Entry to handle Account Balance and Stock Value mismatch
				let journal_entry = frappe.model.get_new_doc("FB Journal Entry");
				journal_entry.posting_date = frappe.datetime.get_today();
				
				total_amount = 0;
				frm.doc.distribution.forEach((row) => {
					total_amount += row.amount;
				});

				let child_row = frappe.model.add_child(journal_entry, "jv_details");
				child_row.account = frm.doc.account;
				child_row.credit = total_amount;
				
				frm.doc.distribution.forEach((row) => {
					let child_row = frappe.model.add_child(journal_entry, "jv_details");
					child_row.account = frm.doc.account;
					child_row.against_employee = row.employee;
					child_row.debit = row.amount;
				});


				frappe.set_route("Form", "FB Journal Entry", journal_entry.name);
			});		
		});
	},
});
