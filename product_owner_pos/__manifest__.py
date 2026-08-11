# -*- coding: utf-8 -*-
{
    'name': "Product Owner POS",
    'version': "19.0.1.0.0",
    'category': "POS",
    'author': "Cybrosys Technology",
    'license': "LGPL-3",
    'application': True,
    'sequence': -1,
    'depends': ['base','pos_restaurant'],
    'data': ["views/product_template.xml",
             ],
    'assets': {
        'point_of_sale._assets_pos': [
        'product_owner_pos/static/src/js/pos_order.js',
        'product_owner_pos/static/src/js/pos_order_line.js',
        'product_owner_pos/static/src/xml/pos_orderline.xml',]}
}