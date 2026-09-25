from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        if self.env.context.get('skip_minimarket_stock_warning'):
            return super().action_confirm()

        for order in self:
            insufficient_lines = order.order_line.filtered(
                lambda line:
                    line.product_id
                    and line.product_uom_qty > line.product_id.qty_available
            )

            if insufficient_lines:
                wizard = self.env['minimarket.sale.stock.warning.wizard'].create({
                    'sale_order_id': order.id,
                    'line_ids': [
                        (0, 0, {
                            'product_id': line.product_id.id,
                            'requested_qty': line.product_uom_qty,
                            'available_qty': line.product_id.qty_available,
                            'missing_qty': (
                                    line.product_uom_qty -
                                    line.product_id.qty_available
                            ),
                        })
                        for line in insufficient_lines
                    ],
                })

                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Stock insuficiente',
                    'res_model': 'minimarket.sale.stock.warning.wizard',
                    'view_mode': 'form',
                    'res_id': wizard.id,
                    'target': 'new',
                }

        return super().action_confirm()