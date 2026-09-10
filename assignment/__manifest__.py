{
    'name': 'Assignment',
    'version': "19.0.1.0.0",
    'author': "Cybrosys Technology 1.0",
    'license': "LGPL-3",
    'application': True,
    'sequence': -1,
    'depends': ['base', 'sale_management'],
    'data': [
        "security/ir.model.access.csv",
       "wizard/assigment_wizard.xml",
        "views/sale_order.xml",
]
}
