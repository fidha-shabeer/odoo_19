{
    'name': 'Mandatory Attachment',
    # 'summary': "Automated Purchase Order Summary",
    # 'description': "Automated Purchase Order Description",
    'version': "19.0.1.0.0",
    'category': "Purchase",
    'author': "Cybrosys Technology 1.0",
    'license': "LGPL-3",
    'application': True,
    'sequence' : -1,
    'depends': ['base','purchase'],
    'data': [
        "views/res_config_settings_view.xml",
        "views/purchase_order_view.xml",
    ]
}