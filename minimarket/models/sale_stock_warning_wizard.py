from odoo import fields, models


class SaleStockWarningWizard(models.TransientModel):
    _name = 'minimarket.sale.stock.warning.wizard'
    _description = 'Aviso de stock insuficiente en ventas'

    sale_order_id = fields.Many2one(
        'sale.order',
        string='Venta',
        readonly=True,
        required=True,
    )

    line_ids = fields.One2many(
        'minimarket.sale.stock.warning.wizard.line',
        'wizard_id',
        string='Productos',
    )

    def action_cancel(self):
        """Cierra el aviso y mantiene el pedido sin confirmar."""
        return {'type': 'ir.actions.act_window_close'}

    def action_continue(self):
        """Confirma la venta aunque exista stock insuficiente."""
        self.ensure_one()

        return self.sale_order_id.with_context(
            skip_minimarket_stock_warning=True
        ).action_confirm()


class SaleStockWarningWizardLine(models.TransientModel):
    _name = 'minimarket.sale.stock.warning.wizard.line'
    _description = 'Línea de aviso de stock insuficiente'

    wizard_id = fields.Many2one(
        'minimarket.sale.stock.warning.wizard',
        required=True,
        ondelete='cascade',
    )

    product_id = fields.Many2one(
        'product.product',
        string='Producto',
        readonly=True,
    )

    requested_qty = fields.Float(
        string='Solicitado',
        readonly=True,
    )

    available_qty = fields.Float(
        string='Disponible',
        readonly=True,
    )

    missing_qty = fields.Float(
        string='Faltan',
        readonly=True,
    )