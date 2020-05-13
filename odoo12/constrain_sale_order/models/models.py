# -*- coding: utf-8 -*-

from datetime import date, datetime

from odoo import models, fields, api
from odoo.exceptions import ValidationError


# 								inherit 'sale.order'
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Add Constrains in wage
    @api.constrains('partner_id')
    def _check_partner_id(self):
        for record in self:
            if not (record.partner_id.email):
                raise ValidationError('Ingresar correo electronico del cliente.\n')
            if not (record.partner_id.mobile):
                raise ValidationError('Ingresar el numero del telefono movil del cliente.\n')
        return True

    def check_pricelist_date(self, date_today, date_end):
        if date_today >= date_end:
            raise ValidationError('Verificar la fecha de vencimiento en la lista de precio')
        return True

    @api.multi
    def action_confirm(self):
        for record in self:
            if not (record.pricelist_id.active):
                raise ValidationError('Seleccionar una lista de precios que se encuentre activa.\n')
            elif record.pricelist_id.active:
                list_pricelist = [line for line in record.pricelist_id.item_ids]
                list_product = [line for line in record.order_line]
                for line in list_pricelist:
                    if line.date_end:
                        date_end = datetime.strptime(str(line.date_end), '%Y-%m-%d')
                        date_today = datetime.strptime(str(date.today()), '%Y-%m-%d')
                        if line.applied_on == "3_global":
                            self.check_pricelist_date(date_today, date_end)
                        elif line.applied_on == "2_product_category":
                            if line.categ_id in [line.product_id.categ_id for line in list_product]:
                                self.check_pricelist_date(date_today, date_end)
                        elif line.applied_on == "1_product":
                            if line.product_tmpl_id.name in [line.product_id.name for line in list_product]:
                                self.check_pricelist_date(date_today, date_end)
                        elif line.applied_on == "0_product_variant":
                            if line.product_id.name in [line.product_id.name for line in list_product]:
                                self.check_pricelist_date(date_today, date_end)
                        else:
                            pass
                return super(SaleOrder, self).action_confirm()
            else:
                pass



