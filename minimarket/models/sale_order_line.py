
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    minimarket_qty_available = fields.Float(
        string='Disponible',
        related='product_id.qty_available',
        readonly=True,
        help='Cantidad disponible actualmente según el inventario de Odoo.'
    )

    minimarket_cost = fields.Float(
        string='Coste de venta',
        readonly=False,
        help='Coste del producto registrado en el momento de realizar la venta.'
    )

    minimarket_total_cost = fields.Float(
        string='Coste total',
        compute='_compute_minimarket_totals',
        store=True,
        help='Coste histórico total de los productos vendidos en esta línea.'
    )

    minimarket_margin = fields.Float(
        string='Margen',
        compute='_compute_minimarket_totals',
        store=True,
        help='Margen obtenido en esta línea utilizando el coste histórico del producto.'
    )

    minimarket_sale_date = fields.Datetime(
        string='Fecha de venta',
        related='order_id.date_order',
        store=True,
        readonly=True,
        help='Fecha en la que se realizó la venta.'
    )

    minimarket_customer = fields.Many2one(
        string='Cliente',
        related='order_id.partner_id',
        store=True,
        readonly=True,
        help='Cliente asociado a la venta.'
    )

    @api.depends(
        'minimarket_cost',
        'product_uom_qty',
        'price_subtotal'
    )
    def _compute_minimarket_totals(self):
        for line in self:
            line.minimarket_total_cost = (
                line.minimarket_cost * line.product_uom_qty
            )

            line.minimarket_margin = (
                line.price_subtotal
                - line.minimarket_total_cost
            )



