{
    'name': 'Material Request',
    'version': "19.0.1.0.0",
        'category': "Material Request",
    'author': "Cybrosys Technology 1.0",
    'license': "LGPL-3",
    'application': True,
    'sequence' : -1,
    'depends': ['base','sale_management','contacts','stock'],
    'data': [
        "security/ir.model.access.csv",
        "security/security_group.xml",
        "security/material_request_rule.xml",
        "views/material_request.xml",
        "views/material_information.xml",
        "views/material_request_menu.xml",
    ]
}