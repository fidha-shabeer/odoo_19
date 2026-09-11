from odoo import models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        products = self.order_line.mapped("product_id")

        for product in products:
            if product.product_combination & products:
                raise ValidationError("Products cannot be sold together.")

        return super().action_confirm()