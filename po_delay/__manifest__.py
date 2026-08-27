# -*- coding: utf-8 -*-
{
    'name': "PO delay",
    'version': "19.0.1.0.0",
    'category': "Milestone Category",
    'author': "Cybrosys Technology auth",
    'license': "LGPL-3",
    'application': True,
    'sequence' : -1,
    'depends': ['base','purchase'],
    'data': [
             "data/email_template.xml",
        "data/ir_cron_data.xml",
             ],
}