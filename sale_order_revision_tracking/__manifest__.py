{
    'name': 'Sale Order Revision Tracking',
    'version': "19.0.1.0.0",
    'category': "Sale",
    'author': "Cybrosys Technology 1.0",
    'license': "LGPL-3",
    'application': True,
    'sequence': -1,
    'depends': ['base', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order.xml',
        'views/sale_order_revision.xml',
    ]
}
