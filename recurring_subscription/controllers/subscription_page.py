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

        user=request.env.user.partner_id.id if request.env.user.id else 'Guest'
        request.env['recurring.subscription'].create({
            'partner_id': user,
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

    @http.route('/subscription-edit/<int:subscription_id>', type='http',
                auth='public', website=True,
                csrf=False)
    def subscription_edit(self, subscription_id, **kwargs):
        user_name = request.env.user.id if request.env.user.id else 'Guest'
        print(user_name)

        products = request.env['product.product'].search([])
        print("products:", products)

        partners = request.env['res.partner'].search([])
        print("partners:", partners)

        subscription = request.env['recurring.subscription'].browse(
            subscription_id)

        return request.render(
            'recurring_subscription.page_recurring_subscription',
            {
                'user_name': user_name,
                'products': products,
                'partners': partners,
                'subscription': subscription,
            })

    @http.route('/subscription-save-changes/<int:subscription_id>', type='http',auth='public',csrf=False)
    def subscription_save_changes(self, subscription_id, **kwargs):
        user_name = request.env.user.name if request.env.user.id else 'Guest'
        print(user_name)
        partners = request.env['res.partner'].search([])
        print("partners:", partners)
        sub = request.env['recurring.subscription'].browse(int(subscription_id))
        print("sub:", sub)
        if sub:
            sub.write({
                # 'partner_id': sub.partner_id.id,
                'partner_id': request.env.user.id,
                'id_establishment': sub.establishment_id,
                'product_id': sub.product_id.id,
                'date': sub.date,
                'recurring_amount': sub.recurring_amount,
                'is_leads': sub.is_leads,
            })

        return request.render('recurring_subscription.all_subscription_list')

    @http.route('/subscription-delete/<int:subscription_id>', type='http', auth='public',)
    def subscription_delete(self, subscription_id, **kwargs):
        sub = request.env['recurring.subscription'].search([])
        subscription = request.env['recurring.subscription'].browse(int(subscription_id))
        print('subscription_id', subscription)
        if subscription:
            subscription.unlink()
        return request.render('recurring_subscription.page_subscription_success')


