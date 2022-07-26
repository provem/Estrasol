from odoo import models, fields, api
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


    def write(self, vals):
        _logger.info(vals.keys())
        
        if 'order_line' in vals.keys():
            _logger.info(vals['order_line'][0])
        
        _logger.info('------------------------------------------------')
        _logger.info(self.id)
        _logger.info(str(self.amount_total))
        _logger.info(str(self.credit_after_sale))
        _logger.info('------------------------------------------------')
        if self.state == 'draft' and self.partner_has_credit:
             if 'order_line' in vals.keys():
                if len(vals['order_line']) == 1 and vals['order_line'][0][2]['price_unit']* 1.16 > 0:
                    super(InheritedSaleOrder, self).write(vals)
                    self.with_context(skip=True).action_confirm()
        if self._context.get('skip') == True:
            _logger.info('True')
            return super(InheritedSaleOrder, self).write(vals)
        if self._context.get('skip') == False:
            _logger.info('False')
            return super(InheritedSaleOrder, self).write(vals)
        else:
            _logger.info('Último')
            return super(InheritedSaleOrder, self).write(vals)
        
        
    @api.model    
    def create(self, vals):
        res = super(InheritedSaleOrder, self.with_context(skip=False)).create(vals)

        if res.partner_has_credit and res.credit_after_sale < 0:
            res.with_context(skip=True).write({'state': 'draft'})
        elif res.partner_has_credit and res.credit_after_sale > 0:
            res.with_context(skip=False).action_confirm()

        return res