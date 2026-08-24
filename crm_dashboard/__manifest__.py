# __manifest__.py
{
    'name': 'CRM Dashboard',
    'summary': 'CRM Dashboard summary',
    'version': '1.0',
    'depends': ['base', 'crm','sale_management'],
    'application': True,
    'sequence': -1,
    'installable': True,
    'data': [
        'views/crm_team.xml',
        'views/dashboard_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'crm_dashboard/static/src/js/dashboard.js',
            'crm_dashboard/static/src/xml/dashboard.xml',
        ],
    },
}
