from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class InheritedPartner(models.Model):

    _inherit = 'res.partner'

    credit_enabled = fields.Boolean(
        string='¿Aplica crédito disponible?', default=False)
    available_credit = fields.Float(
        string='Crédito Disponible', compute='_compute_available_credit', store=True, readonly=True)

    
    def _compute_available_credit(self):
        for record in self:
            available_credit = record.credit_limit - record.credit
            record.available_credit = available_credit
            _logger.info(str(record.available_credit))
