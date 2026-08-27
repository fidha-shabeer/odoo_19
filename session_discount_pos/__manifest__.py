# __manifest__.py
{
   'name': 'Session Discount POS',
   'version': '1.0',
   'depends': ['base','pos_restaurant'],
   'data': [
       'views/res_config_settings.xml',
       'views/pos_session.xml',
       'views/pos_order.xml',
   ],
    'application': True,
    'sequence': -1,
   'installable': True,
    'assets': {
        'point_of_sale._assets_pos': [
            'session_discount_pos/static/src/js/pos_payment_validation.js',
            'session_discount_pos/static/src/js/pos_order.js',
            'session_discount_pos/static/src/js/pos_validate_order.js',
        ],}
}

