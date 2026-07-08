# -*- coding: utf-8 -*-
{
    'name': "VIP Discount Sales",
    'summary': "VIP Discount Sales",
    'version': "19.0.1.0.0",
    'description': """VIP Discount for VIP customers""",
    'category': "VIP Discount",
    'author': "Cybrosys Technology",
    'license': "LGPL-3",
    'application': True,
    'sequence' : -1,
    'depends': ['base','contacts','sale_management'],
    'data': ["views/res_partner.xml",
             "views/sale_order.xml",
             ],
}