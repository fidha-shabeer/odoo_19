{
    'name': 'User Based Journal Access and Visibility Control',
    'version': "19.0.1.0.0",
    'category': "account",
    'author': "Cybrosys Technology 1.0",
    'license': "LGPL-3",
    'application': True,
    'sequence': -1,
    'depends': ['base', 'account'],
    'data': [
        "security/record_rule.xml",
        "views/res_users.xml",
    ]
}
