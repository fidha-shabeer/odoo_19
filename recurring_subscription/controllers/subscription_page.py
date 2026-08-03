# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class SubscriptionPage(http.Controller):
    @http.route('/recurring-odoo', type='http', auth='public', website=True,
                csrf=False)
    def subscription_page(self, **kwargs):
        user_name = request.env.user.name if request.env.user.id else 'Guest'
        print(user_name)

        products = request.env['product.product'].search([])
        print("products:", products)

        partners = request.env['res.partner'].search([])
        print("partners:", partners)

        subscriptions = request.env['recurring.subscription'].search([])

        return request.render('recurring_subscription.all_subscription_list', {
            'user_name': user_name,
            'products': products,
            'partners': partners,
            'subscriptions': subscriptions,

        })

    @http.route('/recurring-form', type='http', auth='public', website=True)
    def recurring_form(self, **kwargs):
        user_name = request.env.user.name if request.env.user.id else 'Guest'
        print(user_name)

        products = request.env['product.product'].search([])
        print("products:", products)

        partners = request.env['res.partner'].search([])
        print("partners:", partners)
        return request.render(
            'recurring_subscription.page_recurring_subscription', {
                'user_name': user_name,
                'products': products,
                'partners': partners,
            })

    @http.route('/subscription-create', type='http', auth='public',
                website=True, csrf=False)
    def subscription_create(self, **post):
        print('partner_id', post.get('partner_id'))
        print('is_leads', post.get('is_lead'))

        request.env['recurring.subscription'].create({
            'partner_id': post.get('partner_id'),
            'id_establishment': post.get('establishment_id'),
            'product_id': post.get('product_id'),
            'date': post.get('date'),
            'recurring_amount': post.get('recurring_amount'),
            'is_leads': post.get('is_lead'),

        })

        subscriptions = request.env['recurring.subscription'].search([])

        return request.render('recurring_subscription.all_subscription_list', {
            'subscriptions': subscriptions,
        })

    @http.route('/subscription-edit', type='http', auth='public', website=True,
                csrf=False)
    def subscription_edit(self, **post):
        user_name = request.env.user.name if request.env.user.id else 'Guest'
        print(user_name)

        products = request.env['product.product'].search([])
        print("products:", products)

        partners = request.env['res.partner'].search([])
        print("partners:", partners)

        return request.render(
            'recurring_subscription.page_recurring_subscription',
            {
                'user_name': user_name,
                'products': products,
                'partners': partners,
            })
