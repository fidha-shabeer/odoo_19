from odoo import models, fields


class BulkPriceUpdate(models.TransientModel):
    _name = 'bulk.price.update'

    product_ids = fields.Many2many('product.product', string='Products To Update')
    percentage = fields.Float(string='Percentage')
    fixed_price = fields.Float(string='Fixed Price')
    select_id = fields.Selection([
        ('fixed_price', 'Fixed Price'),
        ('percentage', 'Percentage')], default='fixed_price', string='Select Type')
    percent_type = fields.Selection([('increase','Increase'),('decrease','Decrease')], default='increase')

    def action_update_price(self):
        print("update price")
        product_ids = self.product_ids
        print(product_ids)

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
                product.lst_price = fixed_price
                print("updated price", product.lst_price)
            if self.percentage:
                if self.percent_type == 'increase':
                    product.lst_price = percentage * product.lst_price
                    print("updated price", product.lst_price)
                if self.percent_type == 'decrease':
                    decrease = product.lst_price * (percentage/100)
                    print("decrease", decrease)
                    discount_percent = product.lst_price - decrease
                    print("discount_percent", discount_percent)

            product_update = self.env['updated.price'].create({
                'product_id': product.id,
                'original_price': original,
                'updated_price': product.lst_price,
            })
            pro_list.append(product_update.id)
            print(pro_list)
        print("updated price", product_update)
        readd = self.env['updated.price'].search_read([])
        print("readd", readd)

        return {
            'type': 'ir.actions.act_window',
            'name': 'View Updated Price',
            'res_model': 'updated.price',
            'view_mode': 'list',
            'target': 'new',
            'domain': [('id', 'in', pro_list)],
        }

        # return {
        #         'type': 'ir.actions.client',
        #         'tag': 'display_notification',
        #         'params': {
        #             'type': 'Successfully Updated the product price',
        #             'message': f'Successfully Updated the product variant price', }
        #
        #     }

# def action_view_update(self):
#     print("view updated price")
#     product_ids = self.product_ids
#     print(product_ids)
#     for product in product_ids:
#         print("product",product)
#         product = product.id
#         original_price = product.lst_price
#
#     return {
#         'type': 'ir.actions.act_window',
#         'name': 'View Updated Price',
#         'res_model': 'updated.price',
#         'view_mode': 'list',
#         'target': 'new',
#         'context': {
#             'default_product_id': product.id,
#             'default_original_price': self.percentage,
#             'default_fixed_price': self.fixed_price,
#
#         }
#     }
#
