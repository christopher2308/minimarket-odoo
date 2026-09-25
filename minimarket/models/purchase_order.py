from odoo import models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def _has_previous_real_purchase(self, product):
        """
        Comprueba si el producto tiene una compra real anterior
        registrada en Odoo.
        """
        previous_line = self.env['purchase.order.line'].search([
            ('product_id', '=', product.id),
            ('order_id.state', '=', 'purchase'),
            ('order_id', '!=', self.id),
        ], limit=1)

        return bool(previous_line)


    def _get_minimarket_price_changes(self):
        """
        Detecta productos cuyo precio de compra ha cambiado
        respecto al coste actual del producto.
        """
        changes = []

        for order in self:
            for line in order.order_line:

                # Ignoramos líneas que no corresponden a productos.
                if line.display_type:
                    continue

                product = line.product_id

                if not product:
                    continue

                product_template = product.product_tmpl_id

                old_price = product_template.standard_price
                new_price = line.price_unit
                print("MINIMARKET DEBUG - Precio compra:", new_price)

                # Es la funcion anterior de arriba utilizada para comprobar si hubo una compra anterior
                has_previous_purchase = self._has_previous_real_purchase(product)

                # Si ya existe una compra anterior, solo intervenimos
                # cuando el nuevo coste sea diferente no más
                if has_previous_purchase and old_price == new_price:
                    continue

                current_sale_price = product_template.list_price

                if has_previous_purchase and old_price:
                    # Compra posterior: conservamos el margen que tenía el producto.
                    current_margin = (
                        (current_sale_price - old_price) / old_price
                    ) * 100
                else:
                    # Primera compra real: utilizamos el margen inicial de MiniMarket.
                    current_margin = 30.0

                recommended_sale_price = (
                    new_price * (1 + current_margin / 100)
                )

                changes.append({
                    'product_id': product.id,
                    'old_purchase_price': old_price if has_previous_purchase else 0.0,
                    'new_purchase_price': new_price,
                    'current_sale_price': current_sale_price,
                    'current_margin': current_margin,
                    'recommended_sale_price': recommended_sale_price,
                    'sale_price': recommended_sale_price,
                })

        return changes

    def button_confirm(self):
        """
        Revisa los cambios de precio antes de confirmar
        el pedido de compra.
        """
        self.ensure_one()

        changes = self._get_minimarket_price_changes()

        if not changes:
            result = super().button_confirm()

            for line in self.order_line:

                if line.display_type:
                    continue

                product_template = line.product_id.product_tmpl_id

                previous_cost = product_template.standard_price

                product_template.last_purchase_price = previous_cost
                product_template.standard_price = line.price_unit

            return result

        wizard = self.env['minimarket.purchase.price.change.wizard'].create({
            'purchase_order_id': self.id,
        })

        for change in changes:
            print("MINIMARKET DEBUG - Datos del wizard:", change)

            self.env['minimarket.purchase.price.change.wizard.line'].create({
                'wizard_id': wizard.id,
                **change,
            })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Cambio de precio de compra',
            'res_model': 'minimarket.purchase.price.change.wizard',
            'view_mode': 'form',
            'res_id': wizard.id,
            'target': 'new',
        }

    def _confirm_minimarket_purchase(self):
        """
        Continúa la confirmación utilizando el comportamiento estándar
        de Odoo.
        """
        return super().button_confirm()