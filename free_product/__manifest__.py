# -*- coding: utf-8 -*-
{
    'name': "Free Product",
    # 'summary': "Discount Approval",
    'version': "19.0.1.0.0",
    # 'description': """Discount Approval""",
    'category': "Free Product",
    'author': "Cybrosys Technology",
    'license': "LGPL-3",
    'application': True,
    'sequence' : -1,
    'depends': ['base','sale_management'],
    'data': [
        "views/sale_order.xml",
        "views/product_product.xml",
        "views/sale_order_line.xml",
    ],
}