# __manifest__.py
{
   'name': 'Bulk Price Update Wizard',
   'version': '1.0',
   'depends': ['base','sale_management'],
    'application': True,
    'sequence': -1,
   'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'wizard/view_update_wizard.xml',
        'wizard/bulk_price_update_views.xml',
        'views/updated_price.xml',
        'views/sale_menu.xml',
    ]
}

