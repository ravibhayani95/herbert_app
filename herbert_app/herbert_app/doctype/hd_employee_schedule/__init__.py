import frappe

#herbert_app.herbert_app.doctype.hd_employee_schedule.get_employee_no
@frappe.whitelist()
def get_employee_no(name):
    no = ""
    no = name.split("/")
    no = int(no[1])
    return no

@frappe.whitelist()
def get_template_schedules(template):
    return frappe.db.sql("""SELECT day,
                            time_in_am,
                            time_out_am,
                            time_in,
                            time_out FROM `tabHD Employee Schedules`
                            INNER JOIN `tabHD Employee Schedule Template`
                            ON `tabHD Employee Schedule Template`.name=`tabHD Employee Schedules`.parent
                            WHERE  `tabHD Employee Schedule Template`.name=%s
                            AND `tabHD Employee Schedules`.parentfield='schedules'""",(template),as_dict=True)


@frappe.whitelist()
def get_template_holidays(template):
    return frappe.db.sql("""SELECT day,
                            time_in_am,
                            time_out_am,
                            time_in,
                            time_out FROM `tabHD Employee Schedules`
                            INNER JOIN `tabHD Employee Schedule Template`
                            ON `tabHD Employee Schedule Template`.name=`tabHD Employee Schedules`.parent
                            WHERE  `tabHD Employee Schedule Template`.name=%s
                            AND `tabHD Employee Schedules`.parentfield='holidays'""",(template),as_dict=True)