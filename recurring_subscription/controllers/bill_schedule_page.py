# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo import Command

class BillSchedulePage(http.Controller):
    @http.route('/bill-odoo', type='http', auth='public', website=True,csrf=False)
    def bill_page(self, **kwargs):
        user_name = request.env.user.name if request.env.user.id else 'Guest'
        print(user_name)

        subscriptions = request.env['recurring.subscription'].sudo().search([])
        print("subscription:", subscriptions)

        return request.render('recurring_subscription.page_bill_schedule', {
            'user_name': user_name,
            'subscriptions': subscriptions,

        })


    @http.route('/bill-create', type='http', auth='public', website=True,csrf=False)
    def bill_create(self, **post):
        print('subscription_ids',post.get('rec_sub_id'))

        sub = request.env['recurring.subscription'].sudo().search([('id','=',int(post.get('rec_sub_id')))])
        print('subs',sub.partner_id.name)
        request.env['billing.schedule'].sudo().create({
            'subscription_ids': [Command.set([sub.id])],
            'restrict_customers_ids': [Command.set([sub.partner_id.id])],
            'credit_rec_ids' : [Command.set([sub.credits_ids.id])],
            'names': post.get('bill_name'),
            'period' : post.get('period'),

        })
        return request.render('recurring_subscription.page_bill_success')
