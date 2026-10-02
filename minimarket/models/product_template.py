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

    last_purchase_price = fields.Float(
        string='Último precio de compra',
        help='Precio pagado en la última compra registrada para este producto.'
    )

    minimarket_min_stock = fields.Float(
        string='Stock mínimo',
        default=0.0,
        help='Cantidad mínima de unidades que se recomienda mantener en stock. '
             'Si el stock disponible es igual o inferior a este valor, '
             'MiniMarket generará un aviso de reposición.'
    )

    def _check_minimarket_low_stock(self):
        products = self.search([
            ('minimarket_min_stock', '>', 0),
            ('is_storable', '=', True),
        ])

        low_stock_products = []

        for product in products:
            stock_bajo = product.qty_available <= product.minimarket_min_stock

            if stock_bajo:
                low_stock_products.append(product)

        if low_stock_products and self.env.user.email:
            rows = ''

            for product in low_stock_products:
                rows += (
                        '<tr>'
                        '<td>%s</td>'
                        '<td>%.2f</td>'
                        '<td>%.2f</td>'
                        '</tr>'
                        % (
                            product.display_name,
                            product.qty_available,
                            product.minimarket_min_stock,
                        )
                )

            body_html = (
                    '<p>Buenos días,</p>'
                    '<p>Estos productos tienen actualmente un stock '
                    'igual o inferior al mínimo establecido:</p>'
                    '<table border="1" cellpadding="5" cellspacing="0">'
                    '<thead>'
                    '<tr>'
                    '<th>Producto</th>'
                    '<th>Stock disponible</th>'
                    '<th>Stock mínimo</th>'
                    '</tr>'
                    '</thead>'
                    '<tbody>'
                    '%s'
                    '</tbody>'
                    '</table>'
                    '<p>Se recomienda revisar las necesidades de reposición.</p>'
                    % rows
            )

            mail_values = {
                'subject': 'MiniMarket - Informe de stock bajo',
                'body_html': body_html,
                'email_to': self.env.user.email,
            }

            mail = self.env['mail.mail'].sudo().create(mail_values)
            mail.send()

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