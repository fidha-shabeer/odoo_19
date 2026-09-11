# -*- coding: utf-8 -*-
{
    'name': "Demo Testing 1.0",
    'version': "19.0.1.0.0",
    'category': "sales",
    'author': "Cybrosys Technology",
    'license': "LGPL-3",
    'application': True,
    'sequence' : -1,
    'depends': ['base','contacts','sale_management','hr'],
    'data' : [
        # 'data/reference.xml',
        'views/res_partner.xml',
        'views/sale_order_line.xml',
        'views/hr_employee.xml',
        'views/sale_order.xml',
        'views/product_template.xml',
    ]
}