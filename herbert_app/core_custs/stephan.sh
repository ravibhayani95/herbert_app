#!/usr/bin/env bash

root_path="/home/frappe/frappe-bench"
cp $root_path/apps/herbert_app/herbert_app/core_custs/erpnext/salary_register/salary_register.py $root_path/apps/erpnext/erpnext/hr/doctype/salary_register/
cp $root_path/apps/herbert_app/herbert_app/core_custs/erpnext/salary_slip/salary_slip.py $root_path/apps/erpnext/erpnext/hr/doctype/salary_slip/

cd &&
cd frappe-bench &&
rm -f $root_path/apps/erpnext/erpnext/hr/doctype/salary_register/salary_register.pyc &&
rm -f $root_path/apps/erpnext/erpnext/hr/doctype/salary_slip/salary_slip.pyc &&
bench build &&
bench clear-cache &&
bench restart &&
echo "Success!"

#. /home/frappe/frappe-bench/apps/herbert_app/herbert_app/core_custs/stephan.sh