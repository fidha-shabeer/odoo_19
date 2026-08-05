# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class CreditPage(http.Controller):
    @http.route('/credit-odoo', type='http', auth='public', website=True,
                csrf=False)
    def credit_page(self, **kwargs):
        print('user', request.env.user.has_group)
        if request.env.user.has_group('base.group_public'):
            return request.redirect('/credit-form')

        user_name = request.env.user.name if request.env.user.id else 'Guest'
        print(user_name)

        partners = request.env['res.partner'].sudo().search([])
        print("partners:", partners)

        subscriptions = request.env['recurring.subscription'].sudo().search([])
        print("subscription:", subscriptions)

        credits = request.env['recurring.credit'].sudo().search([])

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

        subscriptions = request.env['recurring.subscription'].sudo().search([])
        print("subscription:", subscriptions)
        return request.render('recurring_subscription.page_credit_sub', {
            'user_name': user_name,
            'subscriptions': subscriptions,
        })

    @http.route('/credit-create', type='http', auth='public', website=True,
                csrf=False)
    def credit_create(self, **post):
        print('user', request.env.user.has_group)
        if request.env.user.has_group('base.group_public'):
            request.env['recurring.credit'].create({
                'recurring_sub_id': post.get('rec_sub_id'),
                'credit_amounts': post.get('credit_amount'),
                'period': post.get('period'),
            })

            return request.redirect('/credit-odoo')
        user_name = request.env.user.name if request.env.user.id else 'Guest'
        print(user_name)

        partners = request.env['res.partner'].sudo().search([])
        print("partners:", partners)

        subscriptions = request.env['recurring.subscription'].sudo().search([])
        print("subscription:", subscriptions)
        credits = request.env['recurring.credit'].sudo().search([])

        request.env['recurring.credit'].create({
            'recurring_sub_id': post.get('rec_sub_id'),
            'credit_amounts': post.get('credit_amount'),
            'period': post.get('period'),
        })
        return request.render('recurring_subscription.all_credit_list', {
            'user_name': user_name,
            'subscriptions': subscriptions,
            'credits': credits,
        })

    @http.route('/credit-edit/<int:credit_id>', type='http', auth='public',
                website=True, csrf=False)
    def subscription_edit(self, credit_id, **kwargs):
        user_name = request.env.user.name if request.env.user.id else 'Guest'
        print(user_name)

        partners = request.env['res.partner'].sudo().search([])
        print("partners:", partners)

        subscriptions = request.env['recurring.subscription'].sudo().search([])
        print("subscription:", subscriptions)

        credit = request.env['recurring.credit'].sudo().browse(credit_id)
        print("credit:", credit)
        print("cred rec", credit.recurring_sub_id.order_seq)

        return request.render(
            'recurring_subscription.page_credit_sub',
            {
                'user_name': user_name,
                'partners': partners,
                'subscriptions': subscriptions,
                'credit': credit,
            })

    @http.route('/credit-save-changes/<int:credit_id>', type='http',
                auth='public', csrf=False, methods=['POST'])
    def credit_save_changes(self, credit_id, **post):
        # user_name = request.env.user.partner_id.name if request.env.user.id else 'Guest'
        # print(user_name)
        # partners = request.env['res.partner'].search([])
        # print("partners:", partners)
        credit = request.env['recurring.credit'].sudo().browse(int(credit_id))
        print("credit:", credit)
        print('*' * 10, post)
        if credit.exists():
            print('adfasdfasdf', post.get('recurring_sub_id'),
                  type(post.get('recurring_sub_id')))
            print('sss :', credit)
            credit.write({
                'recurring_sub_id': int(post.get('rec_sub_id')),
                'credit_amounts': post.get('credit_amount'),
                'period': post.get('period'),
            })
            print('sub :', credit.read())

        return request.redirect('/credit-odoo')
