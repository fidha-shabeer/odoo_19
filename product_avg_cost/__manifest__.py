# -*- coding: utf-8 -*-
{
    'name': "Product Avg Cost",
    'version': "19.0.1.0",
    'description': """Average Purchase Cost of Product""",
    'category': "Recurring Subscription",
    'author': "Cybrosys Technology",
    'license': "LGPL-3",
    'application': True,
    'installable': True,
    'sequence' : -1,
    'depends': ['base','purchase'],
    'data': [
        "views/product.xml",
    ]
}