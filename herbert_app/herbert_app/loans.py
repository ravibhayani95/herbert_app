import frappe

@frappe.whitelist()
def get_loan_due(employee):
    print(employee)
    loans = frappe.db.sql("""SELECT name,loan_amount,monthly_repayment_amount FROM `tabLoan` WHERE
                                                              applicant_type="Employee" and applicant=%s and docstatus=1"""
                          , (employee))
    print(loans)
    loan_reference = None
    print("===================================")
    html = "<table border=1><tr><th>Reference</th><th>Amt</th><th>Bal</th></tr>"
    repayment = 0.0
    for loan in loans:

        # loans_ = frappe.db.sql("""SELECT credit,reference_name FROM `tabJournal Entry Account`
        #                                               WHERE party_type="Employee" AND party=%s AND reference_type="Loan"
        #                                                AND reference_name=%s""", (employee, loan[0]))
        # print(loans_)
        loan_paid = frappe.db.sql("""SELECT SUM(credit),reference_name FROM `tabJournal Entry Account`
                                                  WHERE party_type="Employee" AND party=%s AND reference_type="Loan"
                                                   AND reference_name=%s
                                                   AND account='104-004 - Other Receivables - Employee Cash Advances/Loans - HD'""", (employee, loan[0]))
        print(loan, loan_paid)
        if loan_paid[0][0]:
            if loan_paid[0][0] < loan[1]:
                loan_reference = loan[0]
                repayment = loan[2]
                break
            html+="<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>".format(loan[0],loan[1],loan[1]-loan_paid[0][0])
        else:
            html += "<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>".format(loan[0], loan[1], loan[1])
        print("--------------------------")

    html+="</table>"

    return repayment

@frappe.whitelist()
def get_loan_balances(employee):
    print(employee)
    loans = frappe.db.sql("""SELECT name,loan_amount FROM `tabLoan` WHERE
                                                              applicant_type="Employee" and applicant=%s and docstatus=1"""
                          , (employee))
    print(loans)
    loan_reference = None
    print("===================================")
    html = "<table border=1><tr><th>Reference</th><th>Amt</th><th>Bal</th></tr>"
    for loan in loans:

        # loans_ = frappe.db.sql("""SELECT credit,reference_name FROM `tabJournal Entry Account`
        #                                               WHERE party_type="Employee" AND party=%s AND reference_type="Loan"
        #                                                AND reference_name=%s""", (employee, loan[0]))
        # print(loans_)
        loan_paid = frappe.db.sql("""SELECT SUM(credit),reference_name,SUM(debit) FROM `tabJournal Entry Account`
                                                  WHERE party_type="Employee" AND party=%s AND reference_type="Loan"
                                                   AND reference_name=%s AND docstatus=1
                                                   AND account='104-004 - Other Receivables - Employee Cash Advances/Loans - HD'""", (employee, loan[0]))
        print(loan, loan_paid)
        if loan_paid[0][0]:
            if loan_paid[0][0] < loan[1]:
                loan_reference = loan[0]
                # break
            if loan_paid[0][2]-loan_paid[0][0] > 0.0:
                amt = '{:,.2f}'.format(loan[1])
                bal = '{:,.2f}'.format(loan_paid[0][2]-loan_paid[0][0])
                html+="<tr><td>{0}</td><td align='right'>{1}</td><td align='right'>{2}</td></tr>".format(loan[0],amt,bal)
        else:
            html += "<tr><td>{0}</td><td align='right'>{1}</td><td align='right'>{2}</td></tr>".format(loan[0], loan[1], loan[1])
        print("--------------------------")

    html+="</table>"

    return html


@frappe.whitelist()
def get_loan_status(employee,loan):
    print(employee)
    loans = frappe.db.sql("""SELECT name,loan_amount FROM `tabLoan` WHERE
                              applicant_type="Employee" and applicant=%s and name=%s"""
                          , (employee,loan))
    print(loans)
    loan_reference = None
    print("===================================")
    html = "<table border=1><tr><th>Reference</th><th>Amt</th><th>Bal</th></tr>"
    status = ""
    for loan in loans:

        # loans_ = frappe.db.sql("""SELECT credit,reference_name FROM `tabJournal Entry Account`
        #                                               WHERE party_type="Employee" AND party=%s AND reference_type="Loan"
        #                                                AND reference_name=%s""", (employee, loan[0]))
        # print(loans_)
        loan_paid = frappe.db.sql("""SELECT SUM(credit),reference_name FROM `tabJournal Entry Account`
                                                  WHERE party_type="Employee" AND party=%s AND reference_type="Loan"
                                                   AND reference_name=%s
                                                    AND account='104-004 - Other Receivables - Employee Cash Advances/Loans - HD'""", (employee, loan[0]))
        print(loan, loan_paid)
        if loan_paid[0][0]:
            if loan_paid[0][0] < loan[1] and (loan_paid[0][0] != 0 or loan_paid[0][0] != None):
                loan_reference = loan[0]
                status = "Partially Paid"
                # break
            elif loan_paid[0][0] == 0 or loan_paid[0][0] == None:
                status = "Unpaid"
            html+="<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>".format(loan[0],loan[1],loan[1]-loan_paid[0][0])
        else:
            html += "<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>".format(loan[0], loan[1], loan[1])
        print("--------------------------")

    html+="</table>"

    return status