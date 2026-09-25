from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    minimarket_qty_available = fields.Float(
        string='Disponible',
        related='product_id.qty_available',
        readonly=True,
        help='Cantidad disponible actualmente según el inventario de Odoo.'
    )