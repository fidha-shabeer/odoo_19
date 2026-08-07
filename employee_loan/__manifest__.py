{
    'name': 'Employee Loan',
    'version': "19.0.1.0.0",
    # 'category': "Purchase",
    'author': "Cybrosys Technology 1.0",
    'license': "LGPL-3",
    'application': True,
    'sequence' : -1,
    'depends': ['base','hr'],
    'data': [
        "security/ir.model.access.csv",
        "data/loan_sequence.xml",
        "views/employee_loan.xml",
        "views/employee_loan_line.xml",
        "views/employee_loan_menu.xml",
    ]
}