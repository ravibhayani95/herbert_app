# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
# Code based from Frappe's Salary Register report, modified by Herbert D. 

#Working Code, with TIN, based on posting date but not sumed up nor sorted

import frappe
from frappe import _
from frappe.utils import flt

import erpnext


def execute(filters=None):
	if not filters: filters = {}
	currency = None
	if filters.get('currency'):
		currency = filters.get('currency')
	company_currency = erpnext.get_company_currency(filters.get("company"))
	salary_slips = get_salary_slips(filters, company_currency)
	if not salary_slips: return [], []

	columns, earning_types, ded_types = get_columns(salary_slips)
	ss_earning_map = get_ss_earning_map(salary_slips, currency, company_currency)
	ss_ded_map = get_ss_ded_map(salary_slips,currency, company_currency)
	doj_map = get_employee_doj_map()

	data = []
	
	for ss in salary_slips:

		# if isinstance(ss.employee, str):
 		#    ss.employee = frappe.get_doc("Employee", ss.employee)
		# commented kay maka cause sa Date of joining and employee nga blank

		row = [ss.name, ss.employee, ss.employee_name, 
			doj_map.get(ss.employee).get('date_of_joining'), 
			# ss.employee.tin if ss.employee else None, 
			doj_map.get(ss.employee).get('tin'), 
			ss.designation,
			ss.start_date, ss.end_date, ]

		if ss.designation is not None: columns[5] = columns[5].replace('-1','120') 


		for e in earning_types:
			row.append(ss_earning_map.get(ss.name, {}).get(e))

		if currency == company_currency:
			row += [flt(ss.gross_pay) * flt(ss.exchange_rate)]
		else:
			row += [ss.gross_pay]

		for d in ded_types:
			row.append(ss_ded_map.get(ss.name, {}).get(d))

		row.append(ss.total_loan_repayment)

		if currency == company_currency:
			row += [flt(ss.total_deduction) * flt(ss.exchange_rate), flt(ss.net_pay) * flt(ss.exchange_rate)]
		else:
			row += [ss.total_deduction, ss.net_pay]
		row.append(currency or company_currency)
		data.append(row)

	return columns, data

def get_columns(salary_slips):
	"""
	columns = [
		_("Salary Slip ID") + ":Link/Salary Slip:150",
		_("Employee") + ":Link/Employee:120",
		_("Employee Name") + "::140",
		_("Date of Joining") + "::80",
		_("Branch") + ":Link/Branch:120",
		_("Department") + ":Link/Department:120",
		_("Designation") + ":Link/Designation:120",
		_("Company") + ":Link/Company:120",
		_("Start Date") + "::80",
		_("End Date") + "::80",
		_("Leave Without Pay") + ":Float:130",
		_("Payment Days") + ":Float:120",
		_("Currency") + ":Link/Currency:80"
	]
	"""
	columns = [
		_("Salary Slip ID") + ":Link/Salary Slip:150",
		_("Employee") + ":Link/Employee:120",
		_("Employee Name") + "::140",
		_("Date of Joining") + ":Date:100",
		_("TIN") + "::120", 
		# _("Branch") + ":Link/Branch:-1",
		# _("Department") + ":Link/Department:-1",
		_("Designation") + ":Link/Designation:120",
		# _("Company") + ":Link/Company:120",
		_("Start Date") + "::100",
		_("End Date") + "::100",
		# _("Leave Without Pay") + ":Float:50",
		# _("Payment Days") + ":Float:120"
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
	if filters.get("employee"): conditions += " and employee = %(employee)s"
	if filters.get("currency") and filters.get("currency") != company_currency:
		conditions += " and currency = %(currency)s"

	return conditions, filters

# Original Frappe Code
# def get_employee_doj_map():
# 	return	frappe._dict(frappe.db.sql("""
# 				SELECT
# 					employee,
# 					date_of_joining,
# 					tin
# 				FROM `tabEmployee`
# 				"""))

def get_employee_doj_map():
    doj_map = {}
    for e in frappe.get_all('Employee', fields=['name', 'date_of_joining', 'tin']):
        doj_map[e.name] = {'date_of_joining': e.date_of_joining, 'tin': e.tin}
    return doj_map


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

