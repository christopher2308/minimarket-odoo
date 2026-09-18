from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    minimarket_location = fields.Char(
        string='Ubicación en tienda',
        help='Indica dónde se encuentra el producto dentro del minimarket.'
    )

    minimarket_margin = fields.Float(
        string='Margen (%)',
        compute='_compute_minimarket_margin',
        store=True,
        help='Margen porcentual calculado sobre el coste del producto. '
             'Se obtiene comparando el precio de venta con el coste.'
    )


    @api.depends('standard_price', 'list_price')
    def _compute_minimarket_margin(self):
        for product in self:
            if product.standard_price:
                product.minimarket_margin = (
                    (product.list_price - product.standard_price)
                    / product.standard_price
                ) * 100
            else:
                product.minimarket_margin = 0.0

    @api.constrains('standard_price', 'list_price')
    def _check_minimarket_sale_price(self):
        for product in self:
            if product.list_price < product.standard_price:
                raise ValidationError(
                    'El precio de venta no puede ser inferior al coste del producto.\n\n'
                    'Producto: %s\n'
                    'Coste: %.2f €\n'
                    'Precio de venta: %.2f €'
                    % (
                        product.display_name,
                        product.standard_price,
                        product.list_price,
                    )
                )