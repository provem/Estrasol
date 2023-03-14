from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class InheritedPartner(models.Model):

    _inherit = 'res.partner'

    credit_enabled = fields.Boolean(
        string='¿Aplica crédito disponible?', default=False)
    provem_available_credit = fields.Float(
        string='Crédito Disponible', compute='_compute_provem_available_credit', store=True, readonly=True)

    @api.depends('sale_order_ids', 'sale_order_ids.state', 'credit_enabled', 'credit_limit')
    def _compute_provem_available_credit(self):
        for record in self:
            used_credit = 0.0
            for sale_order in record.sale_order_ids:
                if sale_order.invoice_status == 'to invoice' and sale_order.state == 'sale':
                    used_credit = used_credit + sale_order.amount_total
                    _logger.info('sale_order.amount_total')
                    _logger.info('-----------------------')
                    _logger.info(sale_order.invoice_status)
                    _logger.info(str(sale_order.id))
                    _logger.info(str(sale_order.amount_total))
                    _logger.info('-----------------------')
            record.provem_available_credit = round(record.credit_limit - used_credit)

    def get_provem_available_credit(self):
        for record in self:
            _logger.info(str(len(record.sale_order_ids)))
            return record.provem_available_credit