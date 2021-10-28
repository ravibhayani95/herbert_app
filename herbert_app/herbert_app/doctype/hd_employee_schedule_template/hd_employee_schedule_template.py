# -*- coding: utf-8 -*-
# Copyright (c) 2019, John Vincent Fiel and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document


class HDEmployeeScheduleTemplate(Document):

    def get_holidays(self):
        print("get holidays")

        holiday = frappe.db.sql("""SELECT name FROM `tabHoliday List` WHERE '{0}' BETWEEN from_date AND to_date""".format(self.date))

        print(holiday)

        holiday_doc = frappe.get_doc("Holiday List",holiday[0][0])

        for hol in holiday_doc.holidays:
            nl = self.append('holidays', {})
            nl.date = hol.holiday_date

    def apply(self):
        print("Apply")
        branch_sql = "branch = '{0}'".format(self.branch)
        department_sql = "department = '{0}'".format(self.department)
        conditions = ""

        if self.branch:
            conditions += branch_sql

        if self.department:
            conditions += "AND " + department_sql

        sql  = """SELECT name FROM `tabEmployee` WHERE status='Active' """+conditions
        employees = frappe.db.sql(sql)
        print(sql)
        print(employees)
        if employees == ():
            frappe.throw("No employees.")


        schedules = []

        for sched in self.schedules:
            schedules.append({"day":sched.day,"time_in_am":sched.time_in_am,"time_out_am":sched.time_out_am,
                              "time_in":sched.time_in,"time_out":sched.time_out})

        holidays = []

        for sched in self.holidays:
            holidays.append({"date":sched.date,"time_in_am":sched.time_in_am,"time_out_am":sched.time_out_am,
                              "time_in":sched.time_in,"time_out":sched.time_out})


        from herbert_app.herbert_app.doctype.hd_employee_schedule import get_employee_no

        for emp in employees:

            sched = frappe.db.sql("""SELECT name FROM `tabHD Employee Schedule` WHERE name=%s""",(get_employee_no(emp[0])))

            if sched == ():
                pass
            else:
                frappe.get_doc("HD Employee Schedule",sched[0][0]).delete()
                frappe.db.commit()

            frappe.get_doc({"doctype": "HD Employee Schedule",
                            "employee_name": emp[0],
                            "employee": get_employee_no(emp[0]),
                            "schedules": schedules,
                            "holidays": holidays,
                            "template": self.name}).insert()