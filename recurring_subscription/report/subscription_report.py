from datetime import timedelta
from odoo import models, api,fields

class SubscriptionReport(models.AbstractModel):
    _name = 'report.recurring_subscription.subscription_report_details'
    _description = 'Subscription Report Details'

    @api.model
    def _get_report_values(self, docids, data=None):
        subscriptions_ids = data.get('subscriptions_ids',
                                         []) if data else []
        subscriptions = self.env['recurring.subscription'].browse(
                subscriptions_ids)
        print("wer aaaaa", subscriptions)
        print("subscriptions_ids", subscriptions_ids)
        latest_terms = self.env['recurring.subscription'].search([],order = 'order_seq desc',limit = 1)
        print("latest_terms", latest_terms)

        customer_filter = subscriptions.mapped('partner_id')
        print("customer_filter", customer_filter)
        same_customer = len(set(customer_filter))==1
        print("same_customer", same_customer)

        product_filter = subscriptions.mapped('product_id')
        print("product_filter", product_filter)
        same_product = len(set(product_filter))==1
        print("same_product", same_product)

        return {
            'doc_ids': subscriptions_ids,
            'doc_model': 'recurring.subscription',
            'docs': subscriptions,
            'report_type': data.get('report_type', '') if data else '',
            'subscription_ids': data.get('subscription_ids',
                                            'All Subscriptions') if data else 'All Subscriptions',
            'latest_terms' : latest_terms,
            'same_customer' : same_customer,
            'same_product' : same_product,
            }