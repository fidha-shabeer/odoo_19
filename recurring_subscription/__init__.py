# -*- coding: utf-8 -*-
from . import models

def post_init_hook(env):
   """Create a default demo product after module installation."""
   ProductTemplate = env['product.template']
   existing = ProductTemplate.search([('default_code', '=', 'SubscriptionCredit')], limit=1)
   if not existing:
       ProductTemplate.create({
           'name': 'Recurring Subscription',
           'default_code': 'SubscriptionCredit',
           'type': 'service',
       })