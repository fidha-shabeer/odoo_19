# -*- coding: utf-8 -*-
from odoo import http
from odoo.exceptions import AccessError
from odoo.http import request
from odoo import Command

class BillSchedulePage(http.Controller):
    @http.route('/bill-odoo', type='http', auth='public', website=True,csrf=False)
    def bill_page(self, **kwargs):

        if not request.env.user.has_group('recurring_subscription.subscription_manager'):
            raise AccessError("Only managers can access this page.")

        user_name = request.env.user.name if request.env.user.id else 'Guest'
        print(user_name)

        subscriptions = request.env['recurring.subscription'].sudo().search([])
        print("subscription:", subscriptions)
        # raw_tag_ids = request.params.get('tag_ids_hidden')
        # tag_ids = []
        # if raw_tag_ids:
        #     try:
        #         tag_ids = list(map(int, raw_tag_ids.split(',')))
        #     except ValueError:
        #         tag_ids = []

        return request.render('recurring_subscription.page_bill_schedule', {
            'user_name': user_name,
            'subscriptions': subscriptions,

        })


    @http.route('/bill-create', type='http', auth='public', website=True,csrf=False)
    def bill_create(self, **post):
        print('subscription_ids',post.get('rec_sub_id'))

        sub = request.env['recurring.subscription'].sudo().search([('id','=',int(post.get('rec_sub_id')))])
        print('subs',sub.partner_id.name)
        print("amt",sum(sub.mapped('credits_ids.credit_amounts')))
        amt = sum(sub.mapped('credits_ids.credit_amounts'))

        bill= request.env['billing.schedule'].sudo().create({
            'subscription_ids': [Command.set([sub.id])],
            'restrict_customers_ids': [Command.set([sub.partner_id.id])],
            'credit_rec_ids' : [Command.set([sub.credits_ids.id])],
            'names': post.get('bill_name'),
            'period' : post.get('period'),
            'total_credits': amt,
        })

        print("bill",bill)
        bill.action_billing()

        return request.render('recurring_subscription.page_bill_success')
