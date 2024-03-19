# Copyright (c) 2015, Frappe Technotinlogies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
# Code based from Frappe's Salary Register report, modified by Herbert D. 
# Working filters for department, with TIN tickbox, summed up, with base rates
 
 

import frappe
from frappe import _
from frappe.utils import flt

import erpnext

def execute(filters=None):
    if not filters:
        filters = {}
    currency = None
    if filters.get('currency'):
        currency = filters.get('currency')
    company_currency = erpnext.get_company_currency(filters.get("company"))
    salary_slips = get_salary_slips(filters, company_currency)
    if not salary_slips:
        return [], []

    columns, earning_types, ded_types = get_columns(salary_slips)
    ss_earning_map = get_ss_earning_map(salary_slips, currency, company_currency)
    ss_ded_map = get_ss_ded_map(salary_slips, currency, company_currency)
    doj_map = get_employee_doj_map() 

    employee_data = {}

    for ss in salary_slips:
        if filters.get('filter_tin') and not doj_map.get(ss.employee).get('tin'):
            continue
        if ss.employee not in employee_data: 

            if filters.get('mwe') == 'MWE' and get_latest_base_rate(ss.employee, filters.get('to_date')) > 435.00:
                continue
            if filters.get('mwe') == 'Non-MWE' and get_latest_base_rate(ss.employee, filters.get('to_date')) <= 435.00:
                continue

            employee_data[ss.employee] = {
                'name': ss.employee_name,
                'department': ss.department,
                'doj': doj_map.get(ss.employee).get('date_of_joining'),
                'tin': doj_map.get(ss.employee).get('tin'),
                'designation': ss.designation,
                'base_rate': get_latest_base_rate(ss.employee, filters.get('to_date')),     
                'earnings': {e: 0 for e in earning_types},
                'gross_pay': 0,
                'deductions': {d: 0 for d in ded_types},
                'total_loan_repayment': 0,
                'total_deduction': 0,
                'net_pay': 0,
            }


        for e in earning_types:
            value = ss_earning_map.get(ss.name, {}).get(e)
            if value is None:
                value = 0
            employee_data[ss.employee]['earnings'][e] += value

        if currency == company_currency:
            employee_data[ss.employee]['gross_pay'] += flt(ss.gross_pay) * flt(ss.exchange_rate)
        else:
            employee_data[ss.employee]['gross_pay'] += ss.gross_pay

        for d in ded_types:
            value = ss_ded_map.get(ss.name, {}).get(d)
            if value is None:
                value = 0
            employee_data[ss.employee]['deductions'][d] += value

        employee_data[ss.employee]['total_loan_repayment'] += ss.total_loan_repayment

        if currency == company_currency:
            employee_data[ss.employee]['total_deduction'] += flt(ss.total_deduction) * flt(ss.exchange_rate)
            employee_data[ss.employee]['net_pay'] += flt(ss.net_pay) * flt(ss.exchange_rate)
        else:
            employee_data[ss.employee]['total_deduction'] += ss.total_deduction
            employee_data[ss.employee]['net_pay'] += ss.net_pay

    data = []

    for employee, employee_info in employee_data.items():
        row = [
            employee,
            employee_info['name'],
            employee_info['doj'],
            employee_info['tin'],
            employee_info['designation'],
            employee_info['base_rate'],
        ]

        row += [employee_info['earnings'][e] for e in earning_types]
        row.append(employee_info['gross_pay'])
        row += [employee_info['deductions'][d] for d in ded_types]
        row.append(employee_info['total_loan_repayment'])
        row.append(employee_info['total_deduction'])
        row.append(employee_info['net_pay'])
        row.append(currency or company_currency)

        data.append(row)

    return columns, data


def get_columns(salary_slips):

	columns = [
		_("Employee") + ":Link/Employee:120",
		_("Employee Name") + "::140",
		_("Date of Joining") + ":Date:100",
        _("TIN") + "::120",
		_("Designation") + ":Link/Designation:120",
		_("Base Rate") + ":Currency:80",
	]
    
	salary_components = {_("Earning"): [], _("Deduction"): []}

	for component in frappe.db.sql("""select distinct sd.salary_component, sc.type
		from `tabSalary Detail` sd, `tabSalary Component` sc
		where sc.name=sd.salary_component and sd.amount != 0 and sd.parent in (%s)""" %
		(', '.join(['%s']*len(salary_slips))), tuple([d.name for d in salary_slips]), as_dict=1):
		salary_components[_(component.type)].append(component.salary_component)

	columns = columns + [(e + ":Currency:120") for e in salary_components[_("Earning")]] + \
		[_("Gross Pay") + ":Currency:120"] + [(d + ":Currency:120") for d in salary_components[_("Deduction")]] + \
		[_("Loan Repayment") + ":Currency:120", _("Total Deduction") + ":Currency:120", _("Net Pay") + ":Currency:120"]

	return columns, salary_components[_("Earning")], salary_components[_("Deduction")]


def get_latest_salary_structure_assignment(employee, to_date):
    """
    Returns the latest salary structure assignment for the given employee
    before the specified to_date.
    """
    assignment = frappe.db.get_all('Salary Structure Assignment',
        fields=['name', 'base', 'from_date'],
        filters={
            'employee': employee,
            'docstatus': 1,
            'from_date': ['<=', to_date]
        },
        order_by='from_date desc',
        limit=1
    )

    return assignment[0] if assignment else {}
 

def get_salary_slips(filters, company_currency):
	filters.update({"from_date": filters.get("from_date"), "to_date":filters.get("to_date")})
	conditions, filters = get_conditions(filters, company_currency)
	salary_slips = frappe.db.sql("""select * from `tabSalary Slip` where %s
		order by employee""" % conditions, filters, as_dict=1)

	return salary_slips or []

def get_conditions(filters, company_currency):
	conditions = ""
	doc_status = {"Draft": 0, "Submitted": 1, "Cancelled": 2}

	if filters.get("docstatus"):
		conditions += "docstatus = {0}".format(doc_status[filters.get("docstatus")])

	if filters.get("from_date"): conditions += " and posting_date >= %(from_date)s"
	if filters.get("to_date"): conditions += " and posting_date <= %(to_date)s"
	if filters.get("company"): conditions += " and company = %(company)s"
	if filters.get("department"): conditions += " and department = %(department)s"
	if filters.get("employee"): conditions += " and employee = %(employee)s"
	if filters.get("currency") and filters.get("currency") != company_currency:
		conditions += " and currency = %(currency)s"

	return conditions, filters


def get_employee_doj_map():
    doj_map = {}
    for e in frappe.get_all('Employee', fields=['name', 'date_of_joining', 'tin']):
        doj_map[e.name] = {'date_of_joining': e.date_of_joining, 'tin': e.tin}
    return doj_map

def get_latest_base_rate(employee, to_date):
    sql = """SELECT base FROM `tabSalary Structure Assignment` 
             WHERE employee=%s AND from_date <= %s 
             ORDER BY from_date DESC LIMIT 1"""
    base_rate = frappe.db.sql(sql, (employee, to_date))
    if base_rate:
        return base_rate[0][0]
    else:
        return 0


def get_ss_earning_map(salary_slips, currency, company_currency):
	ss_earnings = frappe.db.sql("""select sd.parent, sd.salary_component, sd.amount, ss.exchange_rate, ss.name
		from `tabSalary Detail` sd, `tabSalary Slip` ss where sd.parent=ss.name and sd.parent in (%s)""" %
		(', '.join(['%s']*len(salary_slips))), tuple([d.name for d in salary_slips]), as_dict=1)

	ss_earning_map = {}
	for d in ss_earnings:
		ss_earning_map.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, 0.0)
		if currency == company_currency:
			ss_earning_map[d.parent][d.salary_component] += flt(d.amount) * flt(d.exchange_rate if d.exchange_rate else 1)
		else:
			ss_earning_map[d.parent][d.salary_component] += flt(d.amount)

	return ss_earning_map

def get_ss_ded_map(salary_slips, currency, company_currency):
	ss_deductions = frappe.db.sql("""select sd.parent, sd.salary_component, sd.amount, ss.exchange_rate, ss.name
		from `tabSalary Detail` sd, `tabSalary Slip` ss where sd.parent=ss.name and sd.parent in (%s)""" %
		(', '.join(['%s']*len(salary_slips))), tuple([d.name for d in salary_slips]), as_dict=1)

	ss_ded_map = {}
	for d in ss_deductions:
		ss_ded_map.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, 0.0)
		if currency == company_currency:
			ss_ded_map[d.parent][d.salary_component] += flt(d.amount) * flt(d.exchange_rate if d.exchange_rate else 1)
		else:
			ss_ded_map[d.parent][d.salary_component] += flt(d.amount)

	return ss_ded_map

