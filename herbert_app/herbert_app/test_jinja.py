import frappe

context = {
    "name": "John Doe",
    "age": 35,
    "job_title": "Software Developer"
}

message_template = "Hello {{ name }}, you are {{ age }} years old and your job title is {{ job_title }}."

message = frappe.render_template(message_template, context)

print(message)
