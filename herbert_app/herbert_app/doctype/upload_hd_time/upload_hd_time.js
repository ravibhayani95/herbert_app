// Copyright (c) 2019, John Vincent Fiel and contributors
// For license information, please see license.txt

frappe.ui.form.on('Upload HD Time', {
	refresh: function(frm) {

	},
	upload_dat:function (frm) {
		return frappe.call({
			method: "read_dat",
			doc: frm.doc,
			callback: function(r, rt) {
				console.log(r);
				// cur_frm.refresh();
				cur_frm.save();
			}
		});
	},
	reload_dat:function (frm) {
		cur_frm.save();
		return frappe.call({
			method: "reload_dat",
			doc: frm.doc,
			freeze: true,
			async:false,
			callback: function(r, rt) {
				console.log(r);
				// cur_frm.refresh();
				cur_frm.save();
			}
		});
	}
});
