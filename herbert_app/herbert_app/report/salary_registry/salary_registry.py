# Copyright (c) 2013, John Vincent Fiel and contributors
# For license information, please see license.txt


import frappe
from frappe.utils import flt
from frappe import _

def execute(filters=None):
    columns, data = [], []

    columns = [
        {"label": "*", 'width': 10, "fieldname": "*"},]

    if not filters.get("for_printing"):
        columns += [
            {"label": "ID", 'width': 180, "fieldname": "name"},
            {"label": "Payroll#", 'width': 150, "fieldname": "payroll_no"},
            {"label": "Project", 'width': 300, "fieldname": "project"},]

    columns += [
        {"label": "Last Name", 'width': 100, "fieldname": "last_name"},
        {"label": "First Name", 'width': 120, "fieldname": "first_name"},
        {"label": "Middle Name", 'width': 100, "fieldname": "middle_name"},
        {"label": "Designation", 'width': 100, "fieldname": "designation"},
        {"label": "Payment Days", 'width': 100, "fieldname": "payment_days"},
        {"label": "LWO", 'width': 100, "fieldname": "leave_without_pay"},
        {"label": "UT", 'width': 100, "fieldname": "undertime_hours"},
        {"label": "OT", 'width': 100, "fieldname": "overtime_hours"},
     ]
    conditions = ""

    if filters.get("department"):
        conditions += " WHERE `tabSalary Slip`.department='{0}'".format(filters.get("department"))

    if conditions:
        conditions += " AND (`tabSalary Slip`.start_date BETWEEN '{0}' AND '{1}')".format(filters.get("period1"),filters.get("period2"))
    else:
        conditions += " WHERE (`tabSalary Slip`.end_date BETWEEN '{0}' AND '{1}')".format(filters.get("period1"),filters.get("period2"))

    if filters.get("project"):
        if conditions:
            conditions += " AND (`tabPayroll Entry`.project = '{0}')".format(filters.get("project"))
        else:
            conditions += " WHERE (`tabPayroll Entry`.project = '{0}')".format(filters.get("project"))

    if filters.get("branch"):
        if conditions:
            conditions += " AND (`tabSalary Slip`.branch = '{0}')".format(filters.get("branch"))
        else:
            conditions += " WHERE (`tabSalary Slip`.branch = '{0}')".format(filters.get("branch"))

    if filters.get("employee"):
        if conditions:
            conditions += " AND (`tabSalary Slip`.employee = '{0}')".format(filters.get("employee"))
        else:
            conditions += " WHERE (`tabSalary Slip`.employee = '{0}')".format(filters.get("employee"))

    if filters.get("payroll_entry"):
        if conditions:
            conditions += " AND (`tabSalary Slip`.payroll_entry = '{0}')".format(filters.get("payroll_entry"))
        else:
            conditions += " WHERE (`tabSalary Slip`.payroll_entry = '{0}')".format(filters.get("payroll_entry"))

    if filters.get("payroll_entry_hd"):
        if conditions:
            conditions += " AND (`tabSalary Slip`.payroll_entry_hd = '{0}')".format(filters.get("payroll_entry_hd"))
        else:
            conditions += " WHERE (`tabSalary Slip`.payroll_entry_hd = '{0}')".format(filters.get("payroll_entry_hd"))

    if filters.get("docstatus"):
        docstatus = 0
        if filters.get("docstatus") == "Draft":
            docstatus = 0
        elif filters.get("docstatus") == "Submitted":
            docstatus = 1
        elif filters.get("docstatus") == "Cancelled":
            docstatus = 2

        if conditions:
            conditions += " AND (`tabSalary Slip`.docstatus = '{0}')".format(docstatus)
        else:
            conditions += " WHERE (`tabSalary Slip`.docstatus = '{0}')".format(docstatus)

    order_by = " ORDER BY `tabEmployee`.last_name ASC, `tabEmployee`.first_name ASC, `tabEmployee`.middle_name ASC"


    sql = """SELECT `tabSalary Slip`.name,`tabEmployee`.first_name,
                            `tabEmployee`.last_name,`tabEmployee`.middle_name,
                             `tabSalary Slip`.payment_days, `tabSalary Slip`.undertime_hours,
                             `tabSalary Slip`.overtime_hours, `tabSalary Slip`.gross_pay,
                             `tabSalary Slip`.total_deduction, `tabSalary Slip`.net_pay,
                             `tabSalary Slip`.status, `tabSalary Slip`.posting_date,
                              `tabPayroll Entry`.project, `tabSalary Slip`.designation,
                              `tabPayroll Entry`.name as payroll_no,
                              `tabSalary Slip`.leave_without_pay
                               FROM `tabSalary Slip`
                            INNER JOIN `tabEmployee`
                            ON `tabSalary Slip`.employee = `tabEmployee`.name
                              INNER JOIN `tabPayroll Entry`
                            ON `tabSalary Slip`.payroll_entry = `tabPayroll Entry`.name

                             """ + conditions + order_by

    print(sql)
    records = frappe.db.sql(sql,as_dict=True)
    if records:
        # current_designation = records[0].designation
        for i, record in enumerate(records):
            # if current_designation != record.designation:
                # data.append({"name":"************************"})
                # current_designation = record.designation
            record.update({"payroll_no": '<a href="/desk#Form/Payroll%20Entry/' + record["payroll_no"] + '">' + record["payroll_no"] + '</a>'})

    sql = """SELECT `tabSalary Slip`.name,`tabEmployee`.first_name,
                                `tabEmployee`.last_name,`tabEmployee`.middle_name,
                                 `tabSalary Slip`.payment_days, `tabSalary Slip`.undertime_hours,
                                 `tabSalary Slip`.overtime_hours, `tabSalary Slip`.gross_pay,
                                 `tabSalary Slip`.total_deduction, `tabSalary Slip`.net_pay,
                                 `tabSalary Slip`.status, `tabSalary Slip`.posting_date,
                                  `tabPayroll Entry HD`.project, `tabSalary Slip`.designation,
                                  `tabPayroll Entry HD`.name as payroll_no,
                                  `tabSalary Slip`.leave_without_pay
                                   FROM `tabSalary Slip`
                                INNER JOIN `tabEmployee`
                                ON `tabSalary Slip`.employee = `tabEmployee`.name
                                  INNER JOIN `tabPayroll Entry HD`
                                ON `tabSalary Slip`.payroll_entry_hd = `tabPayroll Entry HD`.name

                                 """ + conditions + order_by

    print(sql)
    records_ = frappe.db.sql(sql, as_dict=True)
    if records_:
        # current_designation = records[0].designation
        for i, record in enumerate(records_):
            # if current_designation != record.designation:
            # data.append({"name":"************************"})
            # current_designation = record.designation
            record.update({"payroll_no": '<a href="/desk#Form/Payroll%20Entry%20HD/' + record["payroll_no"] + '">' + record[
                "payroll_no"] + '</a>'})

    records += records_

    group_by = " GROUP BY `tabSalary Slip`.designation"

    designation_counts = frappe.db.sql("""SELECT COUNT(*) as total,`tabSalary Slip`.designation
                                  FROM `tabSalary Slip`
                               INNER JOIN `tabEmployee`
                               ON `tabSalary Slip`.employee = `tabEmployee`.name
                                 INNER JOIN `tabPayroll Entry`
                               ON `tabSalary Slip`.payroll_entry = `tabPayroll Entry`.name

                                """ + conditions + group_by,as_dict=True)

    designation_counts += frappe.db.sql("""SELECT COUNT(*) as total,`tabSalary Slip`.designation
                                  FROM `tabSalary Slip`
                               INNER JOIN `tabEmployee`
                               ON `tabSalary Slip`.employee = `tabEmployee`.name
                                 INNER JOIN `tabPayroll Entry HD`
                               ON `tabSalary Slip`.payroll_entry_hd = `tabPayroll Entry HD`.name

                                """ + conditions + group_by,as_dict=True)
    # print(designation_counts)

    if designation_counts:
        for count in designation_counts:
            data.append({"*":"*","name":str(count['designation'])+": "+str(count['total'])})

    data.append({"name": "************************"})


    earning_columns = ['gross_pay']
    deduction_columns = ['total_deduction','net_pay']

    if records:
        current_designation = records[0].designation
        for i,record in enumerate(records):
            if current_designation != record.designation:
                # data.append({"name":"************************"})
                current_designation = record.designation

            earnings = frappe.db.sql("""SELECT salary_component,amount
                                          FROM `tabSalary Detail` WHERE parent=%s AND parentfield='earnings'""",(record.name),as_dict=True)

            for earning in earnings:
                # print earning.salary_component, earning.amount
                # if float(earning.amount) > 0.00:
                record.update({earning.salary_component:flt(earning.amount)})
                # else:
                # record.update({earning.salary_component:0.00})
                if earning.salary_component not in earning_columns:
                    earning_columns.append(earning.salary_component)

            earnings = frappe.db.sql("""SELECT salary_component,amount
                                                    FROM `tabSalary Detail` WHERE parent=%s AND parentfield='deductions'""",
                                     (record.name), as_dict=True)

            for earning in earnings:
                record.update({earning.salary_component: earning.amount})
                if earning.salary_component not in deduction_columns:
                    deduction_columns.append(earning.salary_component)

            data.append(record.update({"*": str(i + 1),
                                       "payroll_no": "<a href='/desk#Form/Payroll%20Entry%20HD/" + record[
                                           "payroll_no"] + "'>" + record["payroll_no"] + "</a>"}))

        for i, record in enumerate(data):
            for earning in earning_columns:
                # print record[earning]
                # print "============================="
                # print record
                if earning not in record:
                    record.update({earning:None})
                    print(earning, "earning not found")
                # else:
                #     if float(record[earning]) > 0.00:
                #         record.update({earning: float(record[earning])})
                #         # pass
                #     else:
                #         record.update({earning: 0.00})
                #     print "earning found"
            for earning in deduction_columns:
                # print record[earning]
                # print "============================="
                # print record
                if earning not in record:
                    record.update({earning: None})
                    print(earning, "earning not found")
                # else:
                #     if float(record[earning]) > 0.00:
                #         record.update({earning: float(record[earning])})
                #         # pass
                #     else:
                #         record.update({earning: 0.00})
                #     print "earning found"
            # data.append(record.update({"*":str(i+1),"payroll_no":"<a href='/desk#Form/Payroll%20Entry%20HD/"+record["payroll_no"]+"'>"+record["payroll_no"]+"</a>"}))

    for earning in earning_columns:
        if earning not in ['gross_pay']:
            columns.append({"label": earning, 'width': 100, "fieldname": earning,
             "fieldtype": "Currency",
             "options": "currency"
             })

    columns += [   {"label": "Gross Pay", 'width': 100, "fieldname": "gross_pay",
         "fieldtype": "Currency",
         "options": "currency"
         }]

    for earning in deduction_columns:
        if earning not in ['total_deduction','net_pay']:
            columns.append({"label": earning, 'width': 100, "fieldname": earning,
                        "fieldtype": "Currency",
                        "options": "currency"
                        })

    # columns = columns + [(e + ":Currency:120") for e in earning_columns] + \
    #           [_("Gross Pay") + ":Currency:120"] + [(d + ":Currency:120") for d in deduction_columns] + \
    #           [_("Loan Repayment") + ":Currency:120", _("Total Deduction") + ":Currency:120",
    #            _("Net Pay") + ":Currency:120"]

    columns +=[
        {"label": "Total Deduction", 'width': 100, "fieldname": "total_deduction",
         "fieldtype": "Currency",
         "options": "currency"
         },
        {"label": "Net Pay", 'width': 100, "fieldname": "net_pay",
         "fieldtype": "Currency",
         "options": "currency"
         },]

    if not filters.get("for_printing"):
        columns += [
             {"label": "Status", 'width': 100, "fieldname": "status"},
             {"label": "Posting Date", 'width': 100, "fieldname": "posting_date"}
        ]


    return columns, data
