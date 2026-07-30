import re
from odoo import models
from odoo.exceptions import ValidationError


class CreditReport(models.AbstractModel):
    _name = 'report.recurring_subscription.credit_report_details'
    _description = 'Credit Report Details'

    def _get_report_values(self, docids, data=None):
        '''get report values'''
        credits_ids = data.get('credits_ids', []) if data else []
        credits = self.env['recurring.credit'].browse(credits_ids)
        if not credits:
            raise ValidationError("No Credits found in the search")
        print("ab  credits",credits)
        print("search",credits_ids)
        for c in credits:
            credit_state = dict(credits._fields['state'].selection).get(c.state)

        cust_filter = credits.mapped('partner_id')
        print("customer_filter", cust_filter)
        same_cust = len(set(cust_filter)) == 1
        print("same_customer", same_cust)

        return {
            'doc_ids': credits_ids,
            'doc_model': 'recurring.credit',
            'docs': credits,
            'state': data.get('state', '') if data else '',
            'sub_id': data.get('sub_id',
                                     'All Subscriptions') if data else 'All Subscriptions',
            'credit_state': credit_state,
            'same_cust': same_cust,
        }
