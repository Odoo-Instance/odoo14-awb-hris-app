from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    potential_field = fields.Selection([('high', 'High'),
                                        ('moderate', 'Moderate'),
                                        ('low', 'Low')],
                                       string="Current Potential")

    performance_field = fields.Selection([('high', 'High'),
                                          ('moderate', 'Moderate'),
                                          ('low', 'Low')],
                                         string="Current Performance")
    appraisal_value_id = fields.One2many('appraisal.value', 'employee_id',
                                         readonly=True)
    period_id = fields.Many2one('appraisal.period',
                                string='Currecnt Appraisal Period')
    start_date = fields.Date(string='Appraisal Start Date')


class AppraisalValues(models.Model):
    _name = "appraisal.value"

    name = fields.Many2one('appraisal.period', string="Appraisal Period")
    category = fields.Selection([('hp_lp', 'Potential Gem'),
                                 ('hp_mp', 'High Potential'),
                                 ('hp_hp', 'Star'),
                                 ('mp_lp', 'Inconsistent Player'),
                                 ('mp_mp', 'Core Player'),
                                 ('mp_hp', 'High Performer'),
                                 ('lp_lp', 'Risk'),
                                 ('lp_mp', 'Average Performer'),
                                 ('lp_hp', 'Solid Performer')],
                                string="Category")
    potential = fields.Selection([('high', 'High'),
                                  ('moderate', 'Moderate'),
                                  ('low', 'Low')],
                                 string="Potential")
    performance = fields.Selection([('high', 'High'),
                                    ('moderate', 'Moderate'),
                                    ('low', 'Low')],
                                   string="Performance")
    employee_id = fields.Many2one('hr.employee')
