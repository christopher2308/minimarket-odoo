from odoo import fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    minimarket_lot_name = fields.Char(
        string='Lote',
        help='Número de lote que se recibirá para este producto.'
    )