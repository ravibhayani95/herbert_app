// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.query_reports["Compensation Report"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("Posted From"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(),-1),
			"reqd": 1,
			"width": "100px"
		},
		{
			"fieldname":"to_date",
			"label": __("Posted To"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
			"width": "100px"
		},
		{
			"fieldname":"employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
			"width": "100px"
		},
		{
			"fieldname":"department",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department",
			"width": "100px"
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"width": "100px",
			"reqd": 1
		},
		{
			"fieldname":"docstatus",
			"label":__("Document Status"),
			"fieldtype":"Select",
			"options":["Draft", "Submitted", "Cancelled"],
			"default": "Submitted",
			"width": "100px"
		},
		{
			"fieldname":"filter_tin",
			"label":__("Employees With TIN Only"),
			"fieldtype":"Check",
			"default": 1,
		},
		{
			"fieldname":"mwe",
			"label":__("Filter MWE's"),
			"fieldtype":"Select",
			"options":["", "MWE", "Non-MWE"],
			"default": "",
			"width": "100px"
		},

	],

	onload: function(report) {
		report.page.add_inner_button(__("Check with Salary Register"), function() {
			var filters = report.get_values();
			frappe.set_route('query-report', 'Salary Register', {company: filters.company});
		});
	}
}

