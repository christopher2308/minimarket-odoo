from odoo import fields, models


class PurchasePriceChangeWizard(models.TransientModel):
    _name = 'minimarket.purchase.price.change.wizard'
    _description = 'Aviso de cambio de precio de compra'

    purchase_order_id = fields.Many2one(
        'purchase.order',
        string='Pedido de compra',
        readonly=True,
    )

    line_ids = fields.One2many(
        'minimarket.purchase.price.change.wizard.line',
        'wizard_id',
        string='Cambios de precio',
    )

    def action_keep_current_price(self):
        """Mantiene los precios de venta actuales."""
        return self._continue_purchase(update_sale_price=False)

    def action_update_sale_price(self):
        """Actualiza los precios de venta elegidos en el wizard."""
        return self._continue_purchase(update_sale_price=True)

    def _continue_purchase(self, update_sale_price=False):
        """
        Aplica la decisión del usuario y continúa
        con la confirmación estándar de Odoo.
        """
        purchase_order = self.purchase_order_id

        for line in self.line_ids:

            product_template = line.product_id.product_tmpl_id

            # Guardamos el coste actual antes de sustituirlo.
            previous_cost = product_template.standard_price

            # Si el usuario ha decidido actualizar el precio de venta,
            # utilizamos el precio que ha elegido en el wizard.
            if update_sale_price:
                product_template.list_price = line.sale_price

            if line.old_purchase_price:
                product_template.last_purchase_price = line.old_purchase_price
            else:
                product_template.last_purchase_price = 0.0

            product_template.standard_price = line.new_purchase_price

        return purchase_order._confirm_minimarket_purchase()