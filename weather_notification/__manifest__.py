# __manifest__.py
{
    'name': 'Weather Notification',
    'version': '1.0',
    'depends': ['base','sale_management','purchase'],
    # 'data': [
    #
    # ],
    'application': True,
    'sequence': -1,
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'weather_notification/static/src/js/systray_icon.js',
            'weather_notification/static/src/xml/systray_icon.xml',
        ]
    }
}
