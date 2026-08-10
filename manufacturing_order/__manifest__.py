# -*- coding: utf-8 -*-
{
    'name': "Manufacturing Order",
    # 'summary': "Delivery Charges",
    # 'description': "Delivery Charges",
    'version': "19.0.1.0.0",
    'category': "manufacturing",
    'author': "Cybrosys Technology",
    'license': "LGPL-3",
    'application': True,
    'sequence' : -1,
    'depends': ['base','mrp'],
    'data': ["views/mrp_production.xml",
             "views/portal_account.xml",
             ],
}