from odoo import models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _order_fields(self, ui_order):
        res=super()._order_fields(ui_order)
        print("res bfr",res)
        res['product_owner_id'] = ui_order.get('product_order_id')
        print("res get",res)
        return res

    # def _loader_params_product_product(self):
    #     result = super()._loader_params_product_product()
    #     print(result)
    #     result['search_params']['fields'].extend(['product_owner_id'])
    #     return result

