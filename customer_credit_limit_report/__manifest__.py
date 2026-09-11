{
    'name': 'Customer Credit Limit Report',
    'version': "19.0.1.0.0",
    'author': "Cybrosys Technology 1.0",
    'license': "LGPL-3",
    'application': True,
    'sequence': -1,
    'depends': ['base','contacts','account'],
    'data': [
        "security/ir.model.access.csv",
        "security/security_group.xml",
        "wizard/credit_limit_report_view.xml",
        "views/res_partner.xml",
        "views/res_config_settings.xml",
        "views/invoice_menu.xml",
    ]
}
