from odoo import fields, models


class EautContact(models.Model):
    _name = 'eaut.contact'
    _description = 'Liên hệ từ website'
    _inherit = ['mail.thread']
    _order = 'id desc'

    name = fields.Char('Họ tên', required=True)
    email = fields.Char('Email')
    phone = fields.Char('Điện thoại')
    subject = fields.Char('Tiêu đề')
    message = fields.Text('Nội dung')
    state = fields.Selection(
        [('new', 'Mới'), ('processing', 'Đang xử lý'), ('done', 'Đã xử lý')],
        'Trạng thái', default='new', required=True, tracking=True, index=True)

    def action_processing(self):
        self.write({'state': 'processing'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_reopen(self):
        self.write({'state': 'new'})