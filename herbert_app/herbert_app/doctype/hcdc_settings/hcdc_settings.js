// Copyright (c) 2024, John Vincent Fiel and contributors
// For license information, please see license.txt

frappe.ui.form.on('HCDC Settings', {
	refresh_payment_ledger: function(frm) {
		frappe.call({
			method:'refresh_payment_ledger',
			doc: frm.doc,
			callback: function(r){
				console.log(r)
			}
		})
	}
});
