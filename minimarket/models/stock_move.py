from odoo import models


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        vals = super()._prepare_move_line_vals(
            quantity=quantity,
            reserved_quant=reserved_quant,
        )

        purchase_line = self.purchase_line_id

        if purchase_line and purchase_line.minimarket_lot_name:
            vals['lot_name'] = purchase_line.minimarket_lot_name

        return vals