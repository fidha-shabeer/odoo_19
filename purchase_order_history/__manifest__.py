# __manifest__.py
{
   'name': 'Purchase Order History',
   'version': '1.0',
   'depends': ['base','purchase'],
    'application': True,
    'sequence': -1,
   'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_order.xml',
        'views/po_tracker.xml',
    ]
}

