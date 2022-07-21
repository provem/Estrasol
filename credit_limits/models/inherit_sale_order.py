from odoo import models, fields, api
class InheritedSaleOrder(models.Model):
    _inherit = 'sale.order'


    partner_has_credit = fields.Boolean(related='partner_id.credit_enabled', readonly=True)
    available_credit = fields.Float(string='Crédito Dispoible',related="partner_id.available_credit", readonly=True, copy=False)
    credit_after_sale = fields.Float(string='Crédito después de la venta', compute='_compute_credit_after_sale', store=True)

    
    @api.depends('amount_total')
    def _compute_credit_after_sale(self):
        for record in self:
            record.credit_after_sale = record.available_credit - record.amount_total


    def write(self, vals):
        if self._context.get('skip'):
            return super(InheritedSaleOrder, self).write(vals)
        if self.state == 'draft' and self.credit_after_sale > 0 and self.partner_has_credit:
            super(InheritedSaleOrder, self).write(vals)
            self.with_context(skip=True).action_confirm()
        else:
            return super(InheritedSaleOrder, self).write(vals)
        
        
    @api.model    
    def create(self, vals):
        res = super(InheritedSaleOrder, self).create(vals)
        if self.env['res.partner'].search([('id','=',vals['partner_id'])]).credit_enabled:
            res.with_context(skip=False).action_confirm()
        return res