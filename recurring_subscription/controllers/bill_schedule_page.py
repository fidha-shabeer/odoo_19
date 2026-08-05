# -*- coding: utf-8 -*-
from odoo import http
from odoo.exceptions import AccessError, ValidationError
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

        bills = request.env['billing.schedule'].sudo().search([])
        print("bills:", bills)

        return request.render('recurring_subscription.all_bill_list', {
            'user_name': user_name,
            'subscriptions': subscriptions,
            'bills': bills,

        })


    @http.route('/bill-create', type='http', auth='public', website=True,csrf=False)
    def bill_create(self, **post):
        print('subscription_ids',post.get('rec_sub_id'))

        sub = request.env['recurring.subscription'].sudo().search([('id','=',post.get('rec_sub_id'))])
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
        # bill.action_billing()

        return request.render('recurring_subscription.page_bill_schedule')

    @http.route('/bill-form-open', type='http', auth='public', website=True,csrf=False)
    def bill_form_open(self, **post):

        user_name = request.env.user.name if request.env.user.id else 'Guest'
        print(user_name)

        subscriptions = request.env['recurring.subscription'].sudo().search([])
        print("subscription:", subscriptions)

        bills = request.env['billing.schedule'].sudo().search([])
        print("bills:", bills)

        return request.render('recurring_subscription.page_bill_schedule',{
            'user_name': user_name,
            'subscriptions': subscriptions,
            'bills': bills,
        })

    @http.route('/bill-submit', type='http', auth='public', website=True,csrf=False)
    def bill_submit(self, **post):
        bill_ids = request.httprequest.form.getlist('bill_ids')
        if not bill_ids:
            raise ValidationError("No bill_ids")

        print("bill_ids:", bill_ids)
        bills = request.env['billing.schedule'].sudo().browse(int(i) for i in bill_ids)
        print("bills:", bills)
        for bill in bills:
            bill.action_billing()

        return request.render('recurring_subscription.page_bill_success')

