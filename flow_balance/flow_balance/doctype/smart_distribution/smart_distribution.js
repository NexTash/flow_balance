// Copyright (c) 2025, NexTash (SMC-PVT) Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on("Smart Distribution", {
	refresh(frm) {
		frm.add_custom_button(__("Get Distribution"), function () {
			frm.call("get_distribution").then(() => {
				frm.reload_doc();
			});
		});
	},
});
