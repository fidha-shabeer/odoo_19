from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BulkPriceUpdate(models.TransientModel):
    _name = 'bulk.price.update'

    updated_ids = fields.One2many(comodel_name='bulk.price.update.line', inverse_name='bulk_id',
                                  string='Updated Price', )
    product_ids = fields.Many2many(comodel_name='product.product', string='Products To Update')
    percentage = fields.Float(string='Percentage')
    fixed_price = fields.Float(string='Fixed Price')
    select_id = fields.Selection([
        ('fixed_price', 'Fixed Price'),
        ('percentage', 'Percentage')], default='fixed_price', string='Select Type', required=True)
    percent_type = fields.Selection([('increase', 'Increase'), ('decrease', 'Decrease')], default='increase')

    def action_update_price(self):
        print("update price")
        product_ids = self.product_ids
        print(product_ids)

        if not self.product_ids:
            raise ValidationError("choose atleast one product")

        percentage = self.percentage
        print("percentage", percentage)

        fixed_price = self.fixed_price
        print("fixed_price", fixed_price)

        percent_type = self.percent_type
        print("percent_type", percent_type)

        pro_list = []
        for product in self.product_ids:
            print(product)
            original = product.lst_price
            print("original_price", original)

            if self.fixed_price:
                new_amount = fixed_price
                print("updated price", product.lst_price)
            if self.percentage:
                if self.percent_type == 'increase':
                    new_amount = product.lst_price * (1 + percentage / 100)
                    print("updated price", new_amount)
                if self.percent_type == 'decrease':
                    new_amount = product.lst_price * (1 - percentage / 100)
                    print("updated price", new_amount)
            product.lst_price = new_amount

            product_update = self.env['updated.price'].create({
                'product_id': product.id,
                'original_price': original,
                'updated_price': new_amount,
            })
            pro_list.append(product_update.id)
        print(pro_list)

        return {
            'type': 'ir.actions.act_window',
            'name': 'View Updated Price',
            'res_model': 'updated.price',
            'view_mode': 'list',
            'target': 'new',
            'domain': [('id', 'in', pro_list)],
        }

    @api.onchange('percentage', 'fixed_price', 'percent_type')
    def _onchange_updated_ids(self):
        if not self.env.user.has_group('sales_team.group_sale_manager'):
            raise ValidationError("only sales manager can update price")
        print("_compute_updated_ids")
        percentage = self.percentage
        print("percentage", percentage)

        fixed_price = self.fixed_price
        print("fixed_price", fixed_price)

        percent_type = self.percent_type
        print("percent_type", percent_type)

        for product in self.product_ids:
            original = product.lst_price
            print("original_price", original)

            if self.fixed_price:
                product_amt = fixed_price
                print("updated price", product_amt)
            if self.percentage:
                if self.percent_type == 'increase':
                    product_amt = product.lst_price * (1 + percentage / 100)
                    print("updated price", product_amt)
                if self.percent_type == 'decrease':
                    product_amt = product.lst_price * (1 - percentage / 100)
                    print("updated price", product_amt)
            if product._origin.id in self.product_ids.ids:
                print("pro id", product._origin.id)
                print("product ids", self.product_ids.ids)
                self.update({
                   'updated_ids': [fields.Command.create({
                        'product_id': product._origin.id,
                        'original_price': original,
                        'updated_price': product_amt,
                    })]
                    })
                print("self.updated_ids",self.updated_ids._origin.ids)

