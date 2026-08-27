# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class ManufactureOrder(http.Controller):
    @http.route('/manufacture_order', type='http', auth='public', website=True,csrf=False)
    def manufacture_order(self, **kwargs):
        print("manufacture_order")
        customer = request.env.user.partner_id
        orders = request.env['mrp.production'].sudo().search([('partner_id', '=', customer.id)])
        print("orders:", orders)

        return request.render('manufacturing_order.manufacture_order_list', {
            'orders': orders,
        })



