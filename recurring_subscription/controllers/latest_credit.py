# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class LatestCredit(http.Controller):
    @http.route('/get_latest_credit', auth="public", type='jsonrpc',
                website=True)
    def get_latest_credit(self):
        """Get the latest credit for the snippet."""
        partner = request.env.user.partner_id
        credits = request.env[
            'recurring.credit'].sudo().search([('partner_id', '=', partner.id)],
                                              order='create_date desc',
                                              )
        print("credits", credits)
        if not credits:
            return {}
        credit_list = []

        for credit in credits:
            credit_list.append({
                'subscription': credit.recurring_sub_id.order_seq,
                'due_date': credit.recurring_sub_id.due_dates,
                'credit_amount': credit.credit_amounts,
                'image': 'recurring_subscription/static/src/image/image.png',
                'url': f'http://localhost:8019/odoo/action-548/{credit.recurring_sub_id.id}?'

            })
        print("credits list", credit_list)
        return credit_list
