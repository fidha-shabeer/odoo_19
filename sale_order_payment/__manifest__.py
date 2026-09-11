{
    'name': 'Sale Order Payment',
    'summary': "Sale Order Payment Summary",
    'description': "Sale Order Payment Description",
    'version': "19.0.1.0.0",
    'category': "Purchase",
    'author': "Cybrosys Technology 1.0",
    'license': "LGPL-3",
    'application': True,
    'sequence' : -1,
    'depends': ['base','sale_management'],
    'data': [
        "views/sale_order.xml",
    ]
}