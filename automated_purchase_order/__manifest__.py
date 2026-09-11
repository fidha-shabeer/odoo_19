{
    'name': 'Automated Purchase Order',
    'summary': "Automated Purchase Order Summary",
    'description': "Automated Purchase Order Description",
    'version': "19.0.1.0.0",
    'category': "Purchase",
    'author': "Cybrosys Technology 1.0",
    'license': "LGPL-3",
    'application': True,
    'sequence' : -1,
    'depends': ['base','purchase','product'],
    'data': [
        "security/ir.model.access.csv",
        "wizard/product_template_click_view.xml",
        "views/product_template.xml",
    ]
}