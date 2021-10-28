// Copyright (c) 2019, John Vincent Fiel and contributors
// For license information, please see license.txt

frappe.ui.form.on('HD Employee Schedule Template', {
	refresh: function(frm) {

	},
	apply: function(frm) {
		frappe.call({
			method: "apply",
			doc: cur_frm.doc,
			callback: function (r) {

			}
		});
	},
	get_holidays: function(frm) {
		frm.doc.holidays = [];
		frappe.call({
			method: "get_holidays",
			doc: cur_frm.doc,
			callback: function (r) {

				cur_frm.save();
			}
		});
	}
});
