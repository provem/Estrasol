from odoo import models, fields, api


class InheritedPartner(models.Model):

    _inherit = 'res.partner'

    credit_enabled = fields.Boolean(
        string='¿Aplica crédito disponible?', default=False)
    available_credit = fields.Float(
        string='Crédito Disponible', compute_sudo=True, compute='_compute_available_credit', store=True)

    @api.depends('sale_order_count', 'credit_limit', 'credit_enabled', 'sale_order_ids')
    def _compute_available_credit(self):
        for record in self:
            available_credit = record.credit_limit - record.credit
            record.available_credit = available_credit
            for sale_order in record.sale_order_ids:
                if sale_order.invoice_status == 'to invoice' and sale_order.state not in ['cancel', 'draft'] and sale_order.payment_term_id.id != 1:
                    record.available_credit -= sale_order.amount_total
