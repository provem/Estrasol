from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class InheritedSaleOrder(models.Model):

    _inherit = 'sale.order'

    partner_has_credit = fields.Boolean(
        related='partner_id.credit_enabled', readonly=True)
    available_credit = fields.Float(
        string='Crédito Dispoible', compute='_compute_available_credit_so', readonly=True, copy=False, store=True)
    credit_after_sale = fields.Float(
        string='Crédito después de la venta', compute='_compute_credit_after_sale', store=True)


    @api.depends('partner_id')
    def _compute_available_credit_so(self):
        for record in self:
            record.available_credit = record.partner_id.available_credit
            _logger.info(str(record.available_credit))


    @api.depends('amount_total', 'order_line.price_total')
    def _compute_credit_after_sale(self):
        for record in self:
            amount = 0.00
            for order in record.order_line:
                amount += order.price_total
        record.credit_after_sale = record.available_credit - amount


    # @api.model
    # def write(self, vals):
    #     if self._context.get('skip'):
    #         super(InheritedSaleOrder, self).write(vals)
    #     if self.state == 'draft' and self.credit_after_sale > 0 and self.partner_has_credit:
    #         super(InheritedSaleOrder, self).write(vals)
    #         self.with_context(skip=True).action_confirm()
    #     else:
    #         super(InheritedSaleOrder, self).write(vals)
    #     self.partner_id._compute_available_credit()

    # @api.model
    # def create(self, vals):
    #     res = super(InheritedSaleOrder, self).create(vals)
    #     partner = self.env['res.partner'].search([('id', '=', vals['partner_id'])])
    #     if partner.credit_enabled and partner.available_credi > 0:
    #         res.with_context(skip=False).action_confirm()
    #     self.partner_id._compute_available_credit()
    #     return res
