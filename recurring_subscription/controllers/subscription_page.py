# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError
from odoo import Command,fields
from datetime import datetime


class SubscriptionPage(http.Controller):
    @http.route('/recurring-odoo', type='http', auth='public', website=True,
                csrf=False)
    def subscription_page(self, **kwargs):
        print('user', request.env.user.has_group)
        if request.env.user.has_group('base.group_public'):
            return request.redirect('/recurring-form')
        user_name = request.env.user.name if request.env.user.id else 'Guest'
        print(user_name)

        products = request.env['product.product'].sudo().search([])
        print("products:", products)

        partners = request.env['res.partner'].sudo().search([])
        print("partners:", partners)

        subscriptions = request.env['recurring.subscription'].sudo().search([])

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

        products = request.env['product.product'].sudo().search([])
        print("products:", products)

        partners = request.env['res.partner'].sudo().search([])
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
        print('user', request.env.user.has_group)
        if request.env.user.has_group('base.group_public'):
            print("ppartner", post.get('partner_id'))
            print("pid_establishment", post.get('establishment_id'))
            print("pis_lead", post.get('is_lead'))
            print("precurring_amount", post.get('recurring_amount'))
            print("pproduct", post.get('product_id'))

            partner = request.env['res.partner'].sudo().search(
                [('name', '=', post.get('partner_id')),
                 ('id_establishments', '=', post.get('establishment_id'))])
            if partner:
                print("found")
            else:
                partner = request.env['res.partner'].sudo().search([('id_establishments', '=', post.get('establishment_id'))])
                print("partner", partner)

                if partner:
                    raise ValidationError('Establishment already exists')
                else:
                    new = request.env['res.partner'].sudo().create({
                        'name': post.get('partner_id'),
                        'id_establishments': post.get('establishment_id'),
                    })
                print("new", new.id)
                print("id", new.id_establishments)
                print(new, "neww")

                request.env['recurring.subscription'].sudo().create({
                    'partner_id': new.id,
                    'id_establishment': post.get('establishment_id'),
                    'product_id': post.get('product_id'),
                    'date': post.get('date'),
                    'recurring_amount': post.get('recurring_amount'),
                    'is_leads': post.get('is_lead'),

                })

            return request.redirect('/recurring-form')
        print(post, 'post')
        print('partner_id', post.get('partner_id'))
        print('is_leads', post.get('is_lead'))

        user = request.env.user.partner_id.id if request.env.user.id else 'Guest'
        request.env['recurring.subscription'].create({
             'partner_id': request.env.user.partner_id.id,
                'id_establishment': post.get('establishment_id'),
                'product_id': int(post.get('product_id')),
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
        user_name = request.env.user.partner_id.name if request.env.user.id else 'Guest'
        print(user_name)

        products = request.env['product.product'].sudo().search([])
        print("products:", products)

        partners = request.env['res.partner'].sudo().search([])
        print("partners:", partners)

        subscription = request.env['recurring.subscription'].sudo().browse(
            subscription_id)

        return request.render(
            'recurring_subscription.page_recurring_subscription',
            {
                'user_name': user_name,
                'products': products,
                'partners': partners,
                'subscription': subscription,
            })

    @http.route('/subscription-save-changes/<int:subscription_id>', type='http',
                auth='public', csrf=False, methods=['POST'])
    def subscription_save_changes(self, subscription_id, **post):
        user_name = request.env.user.partner_id.name if request.env.user.id else 'Guest'
        print(user_name)
        partners = request.env['res.partner'].sudo().search([])
        print("partners:", partners)
        sub = request.env['recurring.subscription'].sudo().browse(
            int(subscription_id))
        print("sub:", sub)
        print('sub product', sub.product_id.display_name)
        print('sub id', sub.id_establishment)
        print('sub amt', sub.recurring_amount)
        print(sub.date, 'sub date')
        product = post.get('product_id')
        print(product)
        print('is_leads', post.get('is_lead'))
        print('recurring_amount', post.get('recurring_amount'))
        print('product', post.get('product_id'))
        print('date', post.get('date'))
        print('id_establishment', post.get('establishment_id'))
        print('*' * 10, post)
        if sub.exists():
            print('adfasdfasdf', post.get('product_id'),
                  type(post.get('product_id')))
            print('sss :', sub)
            sub.write({
                'partner_id': request.env.user.partner_id.id,
                'id_establishment': post.get('establishment_id'),
                'product_id': int(post.get('product_id')),
                'date': post.get('date'),
                'recurring_amount': post.get('recurring_amount'),
                'is_leads': post.get('is_lead'),

            })
            print('sub :', sub.read())

        return request.redirect('/recurring-odoo')

    @http.route('/subscription-delete/<int:subscription_id>', type='http',
                auth='public', csrf=False)
    def subscription_delete(self, subscription_id, **kwargs):
        subscription = request.env['recurring.subscription'].sudo().browse(
            int(subscription_id))
        print('subscription_id', subscription)
        if subscription.exists():
            subscription.unlink()
            print('subscription_id', subscription)

        return request.redirect('/recurring-odoo')

    @http.route('/bill-create', type='http', auth='public', website=True,
                csrf=False ,method=['post'])
    def bill_create(self, **post):
        print("helooooo")
        subscription_ids = request.httprequest.form.getlist('subscription_ids')
        print("subs", subscription_ids)
        if not subscription_ids:
            raise ValidationError("No bill_ids")

        print("bill_ids:", subscription_ids)
        subs = request.env['recurring.subscription'].sudo().browse(
            int(i) for i in subscription_ids)
        print("bills:", subs)
        for sub in subs:
            print("sub:", sub)
            print("Each amt",sub.mapped('credits_ids.credit_amounts'))
            amt = sum(sub.mapped('credits_ids.credit_amounts'))
            print("amt:", amt)

            if sub.status=='confirm':
                bill = request.env['billing.schedule'].sudo().create({
                    'subscription_ids': [Command.set([sub.id])],
                    'restrict_customers_ids': [
                        Command.set([sub.partner_id.id])],
                    'credit_rec_ids': [Command.set(sub.credits_ids.ids)],
                    'total_credits': amt,
                    'period': datetime.now(),
                    'names' : "Bill %s" %sub.id
                })
                print("over")
                # bill.action_billing()

        return request.render('recurring_subscription.page_subscription_success')

        # bill_ids = request.httprequest.form.getlist('bill_ids')
        # if not bill_ids:
        #     raise ValidationError("No bill_ids")
        #
        # print("bill_ids:", bill_ids)
        # bills = request.env['billing.schedule'].sudo().browse(
        #     int(i) for i in bill_ids)
        # print("bills:", bills)
        # for bill in bills:
        #     bill.action_billing()


