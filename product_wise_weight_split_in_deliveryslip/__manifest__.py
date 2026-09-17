# -*- coding: utf-8 -*-
{
    'name': 'Product Wise Weight Split in Delivery Slip',
    'version': "19.0.1.0.0",
    'category': "sale",
    'author': "Cybrosys Technology 1.0",
    'license': "LGPL-3",
    'application': True,
    'sequence' : -1,
    'depends': ['base','stock'],
    'data': [
        "report/delivery_slip_report.xml",
    ]
}