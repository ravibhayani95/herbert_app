
from frappe import _


def get_data():
    return {
        'fieldname': 'payroll_entry_hd',
        'non_standard_fieldnames': {
            'Journal Entry': 'reference_name',
            'Payment Entry HD': 'reference_name',
        },
        'transactions': [
            {
                'items': ['Salary Slip', 'Journal Entry']
            }
        ]
    }
