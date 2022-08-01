from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class InheritedSaleOrder(models.Model):

    _inherit = 'sale.order'

    partner_has_credit = fields.Boolean(
        related='partner_id.credit_enabled', readonly=True)
    available_credit = fields.Float(
        string='Crédito Disponible', related='partner_id.available_credit', readonly=True, copy=False, store=True)
    credit_after_sale = fields.Float(
        string='Crédito después de la venta', compute='_compute_credit_after_sale', store=True)


    @api.depends('amount_total', 'order_line.price_total', 'order_line')
    def _compute_credit_after_sale(self):
        for record in self:
            amount = 0.00
            for order in record.order_line:
                amount += order.price_total
        record.credit_after_sale = record.available_credit - amount


    def write(self, vals):
        partner = self.env['res.partner'].search([('id','=',self.partner_id.id)])
        if self._context.get('skip'):
            return super(InheritedSaleOrder, self).write(vals)
        if self.state == 'draft' and partner.credit_enabled and partner.available_credit > 0:
            super(InheritedSaleOrder, self).write(vals)
            self.with_context(skip=True).action_confirm()
        else:
            return super(InheritedSaleOrder, self).write(vals)
        
        
    @api.model    
    def create(self, vals):
        res = super(InheritedSaleOrder, self.with_context(skip=False)).create(vals)

        if res.partner_has_credit and res.credit_after_sale < 0:
            res.with_context(skip=True).write({'state': 'draft'})
        elif res.partner_has_credit and res.credit_after_sale > 0:
            res.with_context(skip=False).action_confirm()

        return res