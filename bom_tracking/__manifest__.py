# __manifest__.py
{
   'name': 'BOM History',
   'version': '1.0',
   'depends': ['base','mrp','contacts'],
    'application': True,
    'sequence': -1,
   'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'views/mrp_bom.xml',
        'views/bom_tracker.xml',
    ]
}

