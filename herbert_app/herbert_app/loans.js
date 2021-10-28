frappe.ui.form.on("Salary Slip", "onload",
    function(frm) {

        frappe.call({
            method: "herbert_app.herbert_app.loans.get_loan_balances",
            args: {
                "employee": frm.doc.employee
            },
            callback: function (r) {
                console.log(r);
                if (r.message != cur_frm.doc.loan_balances) {
                    cur_frm.set_value("loan_balances", r.message);
                    // cur_frm.save();
                }
            }
        });
    }
);

frappe.ui.form.on("Salary Slip", "get_loan_due",
    function(frm) {

        frappe.call({
            method: "herbert_app.herbert_app.loans.get_loan_due",
            args: {
                "employee": frm.doc.employee
            },
            callback: function (r) {
                console.log(r);
                if (r.message)
                {
                     var newrow = frm.add_child("deductions");
                    newrow.salary_component = "ST Loan Payment";
                    newrow.amount = r.message;
                    refresh_field("deductions");
                }
                // if (r.message != cur_frm.doc.loan_balances) {
                //     cur_frm.set_value("loan_balances", r.message);
                //     // cur_frm.save();
                // }
            }
        });
    }
);