frappe.ui.form.on("Loan", "onload",
    function(frm) {

        // frappe.call({
        //     method: "herbert_app.herbert_app.loans.get_loan_balances",
        //     args: {
        //         "employee": frm.doc.employee
        //     },
        //     callback: function (r) {
        //         console.log(r);
        //         if (r.message != cur_frm.doc.loan_balances) {
        //             cur_frm.set_value("loan_balances", r.message);
        //             // cur_frm.save();
        //         }
        //     }
        // });

         frappe.call({
            method: "herbert_app.herbert_app.loans.get_loan_status",
            args: {
                "employee": frm.doc.applicant,
                "loan": frm.doc.name
            },
            callback: function (r) {
                console.log(r);
                if (r.message != cur_frm.doc.loan_status) {
                    cur_frm.set_value("loan_status", r.message);
                    // cur_frm.save();
                }
            }
        });
    }
);