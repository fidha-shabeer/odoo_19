# __manifest__.py
{
   'name': 'Session Discount POS',
   'version': '1.0',
   'depends': ['base','pos_restaurant'],
   'data': [
       'views/res_config_settings.xml',
       'views/pos_session.xml',
   ],
    'application': True,
    'sequence': -1,
   'installable': True,
    'assets': {
        'point_of_sale._assets_pos': [
            'session_discount_pos/static/src/js/order_payment_validation.js'],}
}

