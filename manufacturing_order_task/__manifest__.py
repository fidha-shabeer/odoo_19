{
    'name': 'Manufacturing Order Task',
    'version': "19.0.1.0.0",
    'author': "Cybrosys Technology 1.0",
    'license': "LGPL-3",
    'application': True,
    'sequence': -1,
    'depends': ['base','sale_management','mrp'],
    'data': [
        'security/ir.model.access.csv',
        'data/order_sequence.xml',
        'views/mrp_production_ext.xml',
        'views/mrp_production_material_line.xml',
        'views/manufacturing_order_task_menu.xml',
    ]
}
