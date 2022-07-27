from odoo import models, fields, api


class InheritedPartner(models.Model):

    _inherit = 'res.partner'

    credit_enabled = fields.Boolean(string='¿Aplica crédito disponible?', default=False)
    available_credit = fields.Float(string='Crédito Disponible', compute='_compute_available_credit', store=True)

    @api.depends('sale_order_ids', 'credit_limit', 'credit_enabled')
    def _compute_available_credit(self):
        for record in self:
            record.available_credit = record.credit_limit - record.credit
            for sale_order in record.sale_order_ids:
                if sale_order.invoice_status == 'to invoice' and sale_order.payment_term_id.id not in [1, False]:
                    record.available_credit -= sale_order.amount_total