# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AppraisalMenu(models.Model):
    _name = "appraisal.menu"
    _description = "Appraisal Menu"
    _rec_name = "name"

    name = fields.Char(string="Appraisal Period")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")

    @api.model
    def create(self, vals):
        values = {
            'name': vals['name'],
            'start_date': vals['start_date'],
            'end_date': vals['end_date'],
        }
        appraisal_period_id = self.env['appraisal.period'].create(values)
        employee_id = self.env['hr.employee'].search([])
        for rec in employee_id:
            val = {
                'period_id': appraisal_period_id.id,
                'employee_id': rec.id,
                'name': rec.name
            }
            period_id = self.env['period'].create(val)
        return super(AppraisalMenu, self).create(vals)
