from odoo import models, fields, api


class EmployeeList(models.Model):
    _name = "employee.list"

    name = fields.Many2one('hr.employee', string="Employee Name")
    category = fields.Selection([('hp_lp', 'Potential Gem'),
                                 ('hp_mp', 'High Potential'),
                                 ('hp_hp', 'Star'),
                                 ('mp_lp', 'Inconsistent Player'),
                                 ('mp_mp', 'Core Player'),
                                 ('mp_hp', 'High Performer'),
                                 ('lp_lp', 'Risk'),
                                 ('lp_mp', 'Average Performer'),
                                 ('lp_hp', 'Solid Performer')])
    potential = fields.Selection([('high', 'High'),
                                  ('moderate', 'Moderate'),
                                  ('low', 'Low')],
                                 string="Potential")
    performance = fields.Selection([('high', 'High'),
                                    ('moderate', 'Moderate'),
                                    ('low', 'Low')],
                                   string="Performance")
    appraisal_name = fields.Many2one('appraisal.period',
                                     string="Appraisal Periode")
    date = fields.Date(string="Appraisal Date")
    employee_period_id = fields.Many2one('period', string="Employee Period")
