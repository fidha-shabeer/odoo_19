# __manifest__.py
{
    'name': 'CRM',
    'summary': 'Dashboard summary',
    'version': '1.0',
    'depends': ['base','crm','sale_management'],
    'application': True,
    'sequence': -1,
    'installable': True,
    'data': [
        'views/dashboard_menu.xml',
        'views/crm_team.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'dashboard/static/src/js/dashboard.js',
            'dashboard/static/src/xml/dashboard.xml',
            'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.5.1/chart.umd.min.js',

        ],
    },
}
