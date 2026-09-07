# -*- coding: utf-8 -*-
{
    'name': "Product Approval",
    'version': "19.0.1.0.0",
    'category': "project template",
    'author': "Cybrosys Technology",
    'license': "LGPL-3",
    'application': True,
    'sequence': -1,
    'depends': ['base','sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_product.xml',
        'views/product_pricing_notebook.xml',]
}