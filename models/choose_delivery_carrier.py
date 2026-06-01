# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ChooseDeliveryCarrier(models.TransientModel):
    _inherit = 'choose.delivery.carrier'

    # Hacemos editable el campo que se muestra en la vista
    display_price = fields.Float(readonly=False)

    @api.onchange('display_price')
    def _onchange_display_price(self):
        # Al editar manualmente el precio mostrado, sincronizamos
        # delivery_price para que button_confirm use el valor correcto.
        self.delivery_price = self.display_price
