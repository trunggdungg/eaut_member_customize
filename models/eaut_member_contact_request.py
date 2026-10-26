from odoo import fields, models


class EautMemberContactRequest(models.Model):
    _name = 'eaut.member.contact.request'
    _description = 'Yêu cầu liên hệ hội viên'
    _order = 'id desc'

    member_id = fields.Many2one('eaut.member', 'Hội viên', required=True, ondelete='cascade', index=True)
    name = fields.Char('Họ tên', required=True)
    email = fields.Char('Email')
    phone = fields.Char('Điện thoại')
    message = fields.Text('Nội dung')