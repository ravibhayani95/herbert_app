frappe.ui.form.on("Payroll Entry", "onload",
    function(frm) {

     frappe.call({
        method: "herbert_app.herbert_app.payroll_je.get_journals",
        args: {
            "pe": frm.doc.name
        },
        callback: function (r) {
            if (r.message != cur_frm.doc.journal_entries)
            {
                cur_frm.set_value("journal_entries",r.message);
                // cur_frm.save();
            }
        }
    });

         frappe.call({
        method: "herbert_app.herbert_app.payroll_je.check_pe_status",
        args: {
            "pe": frm.doc.name
        },
        callback: function (r) {
            if (r.message != cur_frm.doc.payroll_entry_status)
            {
                cur_frm.set_value("payroll_entry_status",r.message);
                // cur_frm.save();
            }
        }
    });

    }
);