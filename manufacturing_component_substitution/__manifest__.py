{
    'name': 'Manufacturing Component Substitution',
    'version': "19.0.1.0.0",
    'category': "Manufacturing",
    'author': "Cybrosys Technology 1.0",
    'license': "LGPL-3",
    'application': True,
    'sequence' : -1,
    'depends': ['base','mrp'],
    'data': [
        "security/ir.model.access.csv",
        "wizard/alternate_wizard.xml",
        "views/mrp_production.xml",
        "views/product_product.xml",
    ]
}