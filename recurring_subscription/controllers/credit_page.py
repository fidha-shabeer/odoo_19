# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class CreditPage(http.Controller):
    @http.route('/credit-odoo', type='http', auth='public', website=True,csrf=False)
    def credit_page(self, **kwargs):

        user_name = request.env.user.name if request.env.user.id else 'Guest'
        print(user_name)

        partners = request.env['res.partner'].search([])
        print("partners:", partners)

        subscriptions = request.env['recurring.subscription'].search([])
        print("subscription:", subscriptions)

        credits = request.env['recurring.credit'].search([])

        return request.render('recurring_subscription.all_credit_list', {
            'user_name': user_name,
            'subscriptions': subscriptions,
            'credits': credits

        })

    @http.route(['/credit-form'], type='http', auth='public', website=True)
    def credit_form(self, **kwargs):
        user_name = request.env.user.name if request.env.user.id else 'Guest'
        print(user_name)

        partners = request.env['res.partner'].search([])
        print("partners:", partners)

        subscriptions = request.env['recurring.subscription'].search([])
        print("subscription:", subscriptions)
        return request.render('recurring_subscription.page_credit_sub', {
            'user_name': user_name,
            'subscriptions': subscriptions,
        })

    @http.route('/credit-create', type='http', auth='public', website=True,csrf=False)
    def credit_create(self, **post):
        user_name = request.env.user.name if request.env.user.id else 'Guest'
        print(user_name)

        partners = request.env['res.partner'].search([])
        print("partners:", partners)

        subscriptions = request.env['recurring.subscription'].search([])
        print("subscription:", subscriptions)
        credits = request.env['recurring.credit'].search([])

        request.env['recurring.credit'].create({
            'recurring_sub_id': post.get('rec_sub_id'),
            'credit_amounts': post.get('credit_amount'),
            'period' : post.get('period'),
        })
        return request.render('recurring_subscription.all_credit_list',{
            'user_name': user_name,
            'subscriptions': subscriptions,
            'credits': credits,
        })


    @http.route('/credit-edit/<int:credit_id>', type='http',auth='public', website=True,csrf=False)
    def subscription_edit(self, credit_id, **kwargs):
        user_name = request.env.user.name if request.env.user.id else 'Guest'
        print(user_name)

        partners = request.env['res.partner'].search([])
        print("partners:", partners)

        subscriptions = request.env['recurring.subscription'].search([])
        print("subscription:", subscriptions)

        credit = request.env['recurring.credit'].browse(credit_id)
        print("credit:", credit)
        print("cred rec",credit.recurring_sub_id.order_seq)

        return request.render(
            'recurring_subscription.page_credit_sub',
            {
                'user_name': user_name,
                'partners': partners,
                'subscriptions': subscriptions,
                'credit': credit,
            })
