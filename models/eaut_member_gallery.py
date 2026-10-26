from odoo import fields, models


class EautMemberGallery(models.Model):
    _name = 'eaut.member.gallery'
    _description = 'Thư viện ảnh của hội viên'
    _order = 'sequence, id'

    member_id = fields.Many2one('eaut.member', 'Hội viên', required=True, ondelete='cascade', index=True)
    name = fields.Char('Chú thích')
    sequence = fields.Integer(default=10)
    image = fields.Image('Hình ảnh', required=True, max_width=1920, max_height=1920)
    is_published = fields.Boolean('Hiển thị', default=True)