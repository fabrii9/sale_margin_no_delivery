# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    revenue_products = fields.Monetary(
        string="Ingresos (sin envío)",
        compute='_compute_revenue_cost_products',
        store=True,
        groups="base.group_user",
    )
    cost_products = fields.Monetary(
        string="Costo de productos",
        compute='_compute_revenue_cost_products',
        store=True,
        groups="base.group_user",
    )

    @api.depends('order_line.price_subtotal', 'order_line.purchase_price',
                 'order_line.product_uom_qty', 'order_line.is_delivery')
    def _compute_revenue_cost_products(self):
        for order in self:
            non_delivery = order.order_line.filtered(lambda l: not l.is_delivery and not l.display_type)
            order.revenue_products = sum(non_delivery.mapped('price_subtotal'))
            order.cost_products = sum(l.purchase_price * l.product_uom_qty for l in non_delivery)

    @api.depends('order_line.margin', 'order_line.price_subtotal', 'order_line.is_delivery', 'amount_untaxed')
    def _compute_margin(self):
        """
        Sobreescribe el cálculo de margen del módulo sale_margin para excluir
        las líneas de envío (is_delivery=True), ya que el costo de envío
        lo paga el cliente.

        El margen y el porcentaje se calculan únicamente sobre los productos
        vendidos, sin incluir envíos.
        """
        if not all(self._ids):
            # Modo onchange / registros sin guardar
            for order in self:
                non_delivery_lines = order.order_line.filtered(lambda l: not l.is_delivery)
                order.margin = sum(non_delivery_lines.mapped('margin'))
                subtotal = sum(non_delivery_lines.mapped('price_subtotal'))
                order.margin_percent = subtotal and order.margin / subtotal
        else:
            # Recálculo en batch (ej: instalación del módulo) — una sola query
            grouped_data = self.env['sale.order.line']._read_group(
                [
                    ('order_id', 'in', self.ids),
                    ('is_delivery', '=', False),
                ],
                groupby=['order_id'],
                aggregates=['margin:sum', 'price_subtotal:sum'],
            )
            mapped_data = {
                order.id: (margin, subtotal)
                for order, margin, subtotal in grouped_data
            }
            for order in self:
                margin, subtotal = mapped_data.get(order.id, (0.0, 0.0))
                order.margin = margin
                order.margin_percent = subtotal and margin / subtotal
