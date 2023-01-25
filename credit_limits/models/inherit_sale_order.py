from odoo import models, fields, api
from odoo.exceptions import UserWarning
import logging

_logger = logging.getLogger(__name__)


class InheritedSaleOrder(models.Model):

    _inherit = 'sale.order'

    partner_has_credit = fields.Boolean(
        related='partner_id.credit_enabled', readonly=True)
    available_credit = fields.Float(
        string='Crédito Disponible', compute='_compute_available_credit_so', readonly=True, copy=False, store=True)
    credit_after_sale = fields.Float(
        string='Crédito después de la venta', compute='_compute_credit_after_sale', store=True)


    @api.depends('partner_id')
    def _compute_available_credit_so(self):
        for record in self:
            record.available_credit = record.partner_id.available_credit
    
    
    @api.depends('amount_total', 'order_line.price_total', 'order_line')
    def _compute_credit_after_sale(self):
        for record in self:
            amount = 0.00
            for order in record.order_line:
                amount += order.price_total
        record.credit_after_sale = record.available_credit - amount


    def check_permission(self):
        return self.env.user.has_group('credit_limits.overdraft_permission')

    def check_credit(self):
        return self.credit_after_sale >= 0

    def action_confirm(self):
        if self.partner_has_credit:
            if self.payment_term_id in [1,False]:
                return super(InheritedSaleOrder, self).action_confirm()
            if self.check_credit():
                return super(InheritedSaleOrder, self).action_confirm()
            else:
                if self.check_permission():
                    return super(InheritedSaleOrder, self).action_confirm()
                else:
                    raise UserWarning('OOOOPSS')

        else:
            return super(InheritedSaleOrder, self).action_confirm()



        
        
    @api.model    
    def create(self, vals):
        res = super(InheritedSaleOrder, self.with_context(skip=False)).create(vals)

        if res.partner_has_credit and res.credit_after_sale < 0:
            res.with_context(skip=True).write({'state': 'draft'})
        elif res.partner_has_credit and res.credit_after_sale > 0:
            res.with_context(skip=False).action_confirm()

        return res


