{
    'name': "Recurring Subscription",
    'version': "19.0.1.0",
    'summary': """Recurring Subscription""",
    'description': """Recurring Subscription""",
    'author': "Cybrosys Techno Solution",
    'website': "www.cybrosys.com",
    'category': "Recurring Subscription",
    'license': "LGPL-3",
    'depends': ['base','sale_management'],
    'sequence': -10,
    'application': True,
    'installable': True,
    'auto_install': False,
    'data': [
        "security/ir.model.access.csv",
        "data/recurring_sequence.xml",
        "views/recurring_sub.xml",
        "views/subscription_credit_menu.xml",
        "views/recurring_subscription_menus.xml"
    ]
}