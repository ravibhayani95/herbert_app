// Copyright (c) 2019, John Vincent Fiel and contributors
// For license information, please see license.txt

frappe.ui.form.on('HD Employee Schedule', {
	refresh: function(frm) {

	},
		employee_name: function(frm) {

		frappe.call({
			method: "herbert_app.herbert_app.doctype.hd_employee_schedule.get_employee_no",
			args: {
				"name": frm.doc.employee_name
			},
			callback: function (r) {
				cur_frm.set_value("employee",r.message);
			}
		});
	},
	template: function(frm) {
		if (frm.doc.template) {
			frappe.call({
				method: "herbert_app.herbert_app.doctype.hd_employee_schedule.get_template_schedules",
				args: {
					"template": frm.doc.template
				},
				callback: function (r) {
					console.log(r);
					frm.doc.schedules = [];
					for (var i = 0; i < r.message.length; i++) {

						var newrow = frm.add_child("schedules");
						newrow.day = r.message[i].day;
						newrow.time_in_am = r.message[i].time_in_am;
						newrow.time_out_am = r.message[i].time_out_am;
						newrow.time_in = r.message[i].time_in;
						newrow.time_out = r.message[i].time_out;
						refresh_field('schedules');
					}
				}
			});

			frappe.call({
				method: "herbert_app.herbert_app.doctype.hd_employee_schedule.get_template_holidays",
				args: {
					"template": frm.doc.template
				},
				callback: function (r) {
					console.log(r);
					frm.doc.holidays = [];
					for (var i = 0; i < r.message.length; i++) {

						var newrow = frm.add_child("holidays");
						newrow.day = r.message[i].day;
						newrow.time_in_am = r.message[i].time_in_am;
						newrow.time_out_am = r.message[i].time_out_am;
						newrow.time_in = r.message[i].time_in;
						newrow.time_out = r.message[i].time_out;
						refresh_field('holidays');
					}
				}
			});
		}
	}
});
