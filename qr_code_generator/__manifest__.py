# __manifest__.py
{
    'name': 'QR Code Generator',
    'version': '1.0',
    'depends': ['base'],
    # 'data': [
    #     'views/res_users.xml',
    # ],
    'application': True,
    'sequence': -1,
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'qr_code_generator/static/src/js/qr_generator.js',
            'qr_code_generator/static/src/xml/qr_generator.xml',
        ]
    }
}
