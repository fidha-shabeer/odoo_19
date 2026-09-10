# -*- coding: utf-8 -*-
{
    'name': "Milestone Task",
    'summary': "Milestone Task Summary",
    'version': "19.0.1.0.0",
    'description': """Milestone Task Description""",
    'category': "Milestone Category",
    'author': "Cybrosys Technology auth",
    'license': "LGPL-3",
    'application': True,
    'sequence' : -1,
    'depends': ['base','sale_management'],
    'data': ['views/sale_order_view.xml',
        'views/sale_order_line_views.xml',
             ],
}