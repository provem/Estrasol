from odoo import fields, models, api
class InheritedSaleOrderLine(models.Model):

    _inherit = 'sale.order.line'


    @api.onchange('price_subtotal')
    def _onchange_available_credit(self):
        for record in self:
            if record.order_id.credit_after_sale < 0 and len(record.order_id.order_line) > 2 and record.partner_id.credit_enabled:
                record.unlink()