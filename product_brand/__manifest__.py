{
    'name': 'Product Brand',
    'version': "19.0.1.0.0",
    'category': "sale",
    'summary': 'Product Brand',
    'description': "Product Brand Description",
    'author': "Cybrosys Technology 1.0",
    'license': "LGPL-3",
    'application': True,
    'sequence' : -1,
    'depends': ['base','sale_management','product'],
    'data': [
        "security/ir.model.access.csv",
        "views/product_template.xml",
        "views/sale_order_line.xml",
        "views/res_partner.xml",
        "views/sale_order.xml",
        "views/product_brand.xml",
    ]
}