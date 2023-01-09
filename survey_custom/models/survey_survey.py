# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class Survey(models.Model):
    _inherit = 'survey.survey'

    scoring_type_options = fields.Selection([('percentage', 'Survey Percentage'), 
                                ('simple_sum', 'Simple Sum'),
                                ('weighted_sum', 'Weighted Sum'), ('score_name', 'Score Name')], string="Scoring Type", default="percentage")
    score_name_ids = fields.One2many('score.name', 'survey_id', string="Score Names")


# class SurveyLabel(models.Model):
#     """ A suggested answer for a question """
#     _inherit = 'survey.label'

#     question_weight = fields.Float(string="Question Weight")


class SurveyUserInput(models.Model):
    """ Metadata for a set of one user's answers to a particular survey """

    _inherit = "survey.user_input"

    scoring_type_options = fields.Selection(related='survey_id.scoring_type_options', string='Scoring Type')

    @api.depends('user_input_line_ids.answer_score', 'user_input_line_ids.question_id')
    def _compute_quizz_score(self):
        for user_input in self:
            # if user_input.scoring_type_options == 'weighted_sum':
            #     total_possible_score = 0
            #     for rec in user_input.question_ids.mapped('labels_ids'):
            #         total_possible_score += rec.answer_score * rec.question_id.question_weight if rec.answer_score * rec.question_id.question_weight > 0 else 0
            # else:
            total_possible_score = sum([
                answer_score if answer_score > 0 else 0
                for answer_score in user_input.question_ids.mapped('labels_ids.answer_score')
            ])

            if total_possible_score == 0:
                user_input.quizz_score = 0
            else:
                if user_input.scoring_type_options != 'percentage':
                    score = sum(user_input.user_input_line_ids.mapped('answer_score'))
                else:    
                    score = (sum(user_input.user_input_line_ids.mapped('answer_score')) / total_possible_score) * 100
                user_input.quizz_score = round(score, 2) if score > 0 else 0


class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    scoring_type_options = fields.Selection(related='survey_id.scoring_type_options', string='Scoring Type')
    question_weight = fields.Float(string="Question Weight")


class SurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input_line'

    @api.model_create_multi
    def create(self, vals_list):
        records = super(SurveyUserInputLine, self).create(vals_list)
        for rec in records:
            if rec.value_suggested:
                if rec.survey_id.scoring_type_options == 'weighted_sum' or 'score_name':
                    rec.answer_score = (rec.value_suggested.answer_score * rec.question_id.question_weight) / 100    
        return records

    def write(self, vals):
        value_suggested = vals.get('value_suggested')
        if value_suggested:
            if self.env['survey.survey'].browse(int(vals.get('survey_id'))).scoring_type_options == 'weighted_sum' or 'score_name':
                vals.update({'answer_score': (self.env['survey.label'].browse(int(value_suggested)).answer_score * self.question_id.question_weight) / 100})    
            else:
                vals.update({'answer_score': self.env['survey.label'].browse(int(value_suggested)).answer_score})
        return super(SurveyUserInputLine, self).write(vals)


class ScoreName(models.Model):
    _name = 'score.name'

    name = fields.Char('Score Name')
    survey_id = fields.Many2one('survey.survey')
    lower_range = fields.Float('Lower Range')
    upper_range = fields.Float('Upper Range')
