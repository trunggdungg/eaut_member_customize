from odoo import fields, models


class EautMemberService(models.Model):
    _name = 'eaut.member.service'
    _description = 'Dịch vụ của hội viên'
    _order = 'sequence, id'

    member_id = fields.Many2one('eaut.member', 'Hội viên', required=True, ondelete='cascade', index=True)
    name = fields.Char('Tên dịch vụ', required=True)
    sequence = fields.Integer(default=10)
    image = fields.Image('Hình ảnh', max_width=1024, max_height=1024)
    description = fields.Text('Mô tả')
    is_published = fields.Boolean('Hiển thị', default=True)