import frappe

@frappe.whitelist()
def check_pe_status(pe):
    # if frappe.db.sql("""SELECT name FROM `tabPayroll Entry HD` WHERE name=%s""",(pe)):
    #     pe_doc = frappe.get_doc("Payroll Entry HD",pe)
    #     one_not_exists = 0
    #     exist_count = 0
    #     for employee in pe_doc.employees:
    #         exists = frappe.db.sql("""SELECT name FROM `tabSalary Slip`
    #               WHERE payroll_entry_hd=%s AND employee=%s AND docstatus=1""",(pe,employee.employee))
    #
    #         if exists == ():
    #             one_not_exists = 1
    #         else:
    #             exist_count += 1
    #
    #     if one_not_exists == 1 and exist_count > 0:
    #         return "Partially Disbursed"
    #     elif one_not_exists == 0 and exist_count > 0:
    #         return "Fully Disbursed"
    #     elif exist_count == 0:
    #         return None

    total_cred = frappe.db.sql("""SELECT SUM(credit) FROM `tabJournal Entry`
                                INNER JOIN `tabJournal Entry Account`
                                ON `tabJournal Entry Account`.parent = `tabJournal Entry`.name
                                WHERE (voucher_type='Bank Entry' or voucher_type='Cash Entry')
                                AND `tabJournal Entry`.docstatus=1
                                AND `tabJournal Entry Account`.reference_name=%s""",(pe))
    pe_doc = frappe.get_doc("Payroll Entry HD",pe)
    total_pe = 0.0
    for emp in pe_doc.employees:
        net_pay = frappe.db.sql("""SELECT net_pay FROM `tabSalary Slip`
                          WHERE payroll_entry_hd=%s AND employee=%s AND docstatus=1""", (pe, emp.employee))
        if net_pay:
            total_pe += net_pay[0][0]

    if total_cred[0][0] < total_pe and total_cred[0][0] > 0.0:
        return "Partially Disbursed"
    elif total_cred[0][0] >= total_pe:
        return "Fully Disbursed"
    else:
        None


#bench execute herbert_app.herbert_app.payroll_je.test_get_journals
def test_get_journals():
    get_journals("Payroll-S-2019-098")

@frappe.whitelist()
def get_journals(pe):
    salary_slip = frappe.db.sql("""SELECT journal_entry FROM `tabSalary Slip` WHERE payroll_entry_hd=%s""",(pe))
    print(salary_slip)

    html = ""

    for i,slip in enumerate(salary_slip):
        html += str(slip[0]) + "<br>"
        html += "<table border='1' width='100%'>"
        accounts = frappe.db.sql("""SELECT `tabJournal Entry Account`.account,`tabJournal Entry Account`.debit,`tabJournal Entry Account`.credit
                                      FROM `tabJournal Entry Account`
                                      INNER JOIN `tabJournal Entry` ON `tabJournal Entry`.name = `tabJournal Entry Account`.parent
                                      WHERE `tabJournal Entry Account`.parent=%s""",slip[0])
        print(accounts)

        html += "<tr>"
        html += "<th>No.</th>"
        html += "<th>Account</th>"
        html += "<th>Debit</th>"
        html += "<th>Credit</th>"
        html += "</tr>"
        for i,account in enumerate(accounts):
            html += "<tr>"
            html += "<td>" + str(i+1) + "</td>"
            html += "<td>" + account[0] + "</td>"
            html += "<td align='right'>{:,.2f}</td>".format(account[1])
            html += "<td align='right'>{:,.2f}</td>".format(account[2])
            html += "</tr>"

        html += "</table><br>"

    print(html)
    return html