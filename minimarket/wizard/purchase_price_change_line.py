from odoo import api, fields, models


class PurchasePriceChangeWizardLine(models.TransientModel):
    _name = 'minimarket.purchase.price.change.wizard.line'
    _description = 'Línea de cambio de precio de compra'

    wizard_id = fields.Many2one(
        'minimarket.purchase.price.change.wizard',
        string='Wizard',
        required=True,
        ondelete='cascade',
    )

    product_id = fields.Many2one(
        'product.product',
        string='Producto',
        readonly=True,
    )

    old_purchase_price = fields.Float(
        string='Precio de compra anterior',
        readonly=True,
    )

    new_purchase_price = fields.Float(
        string='Nuevo precio de compra',
        readonly=True,
    )

    current_sale_price = fields.Float(
        string='Precio de venta actual',
        readonly=True,
    )

    current_margin = fields.Float(
        string='Margen resultante (%)',
        compute='_compute_current_margin',
        readonly=True,
    )

    recommended_sale_price = fields.Float(
        string='Precio de venta recomendado',
        readonly=True,
    )

    sale_price = fields.Float(
        string='Precio de venta',
        help='Precio de venta que se aplicará al producto al confirmar la decisión.',
    )

    @api.depends('sale_price', 'new_purchase_price')
    def _compute_current_margin(self):
        for line in self:
            if line.new_purchase_price:
                line.current_margin = (
                    (line.sale_price - line.new_purchase_price)
                    / line.new_purchase_price
                ) * 100
            else:
                line.current_margin = 0.0