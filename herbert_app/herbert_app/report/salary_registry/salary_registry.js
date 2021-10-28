// Copyright (c) 2016, John Vincent Fiel and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Salary Registry"] = {
    "filters": [

         {
            "fieldname": "period1",
            "label": __("From Date"),
            "fieldtype": "Date",
             "reqd":1,
            "on_change": function (query_report) {
                console.log(query_report);
                query_report.refresh();
            }
        },
         {
            "fieldname": "period2",
            "label": __("To Date"),
            "fieldtype": "Date",
             "reqd":1,
            "on_change": function (query_report) {
                console.log(query_report);
                query_report.refresh();
            }
        },
        {
            "fieldname": "department",
            "label": __("Department"),
            "fieldtype": "Link",
            "options": "Department",
            // "reqd": 1,
            "on_change": function (query_report) {
                console.log(query_report);
                query_report.refresh();
            }
        },
          {
            "fieldname": "branch",
            "label": __("Branch"),
            "fieldtype": "Link",
            "options": "Branch",
            // "reqd": 1,
            "on_change": function (query_report) {
                console.log(query_report);
                query_report.refresh();
            }
        },
        {
            "fieldname": "project",
            "label": __("Project"),
            "fieldtype": "Link",
            "options": "Project",
            // "reqd": 1,
            "on_change": function (query_report) {
                console.log(query_report);
                query_report.refresh();
            }
        },

          {
            "fieldname": "employee",
            "label": __("Employee"),
            "fieldtype": "Link",
            "options": "Employee",
            // "reqd": 1,
            "on_change": function (query_report) {
                console.log(query_report);
                query_report.refresh();
            }
        }
        ,

          {
            "fieldname": "payroll_entry",
            "label": __("Payroll#"),
            "fieldtype": "Link",
            "options": "Payroll Entry",
            // "reqd": 1,
            "on_change": function (query_report) {
                 frappe.query_report.set_filter_value("payroll_entry_hd", "");
                query_report.refresh();
            }
        }
        ,

          {
            "fieldname": "payroll_entry_hd",
            "label": __("Payroll#HD"),
            "fieldtype": "Link",
            "options": "Payroll Entry HD",
            // "reqd": 1,
            "on_change": function (query_report) {
                 frappe.query_report.set_filter_value("payroll_entry", "");
                query_report.refresh();
            }
        }
        ,
		{
			"fieldname":"docstatus",
			"label":__("Document Status"),
			"fieldtype":"Select",
			"options":["Draft", "Submitted", "Cancelled"],
			"default":"Submitted"
		},
           {
            "fieldname": "for_printing",
            "label": __("Printing"),
            "fieldtype": "Check",
            "on_change": function (query_report) {
                query_report.refresh();
            }
        },

    ]
}
