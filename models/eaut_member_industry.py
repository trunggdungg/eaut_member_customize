from odoo import fields, models


class EautMemberIndustry(models.Model):
    _name = 'eaut.member.industry'
    _description = 'Ngành nghề hội viên'
    _order = 'sequence, name'

    name = fields.Char('Tên ngành', required=True)
    sequence = fields.Integer(default=10)
    member_count = fields.Integer('Số hội viên', compute='_compute_member_count')

    def _compute_member_count(self):
        for industry in self:
            industry.member_count = self.env['eaut.member'].search_count(
                [('industry_id', '=', industry.id)])