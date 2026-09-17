# -*- coding: utf-8 -*-
{
    'name': "Auto Assign Approval Tier by Po Amount",
    'version': "19.0.1.0.0",
    'category': "purchase",
    'author': "Cybrosys Technology",
    'license': "LGPL-3",
    'application': True,
    'sequence': -1,
    'depends': ['base', 'purchase'],
    'data': ['security/security_group.xml',
             'views/purchase_order.xml',]
}
