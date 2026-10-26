from odoo import api, fields, models


class EautMemberPost(models.Model):
    _name = 'eaut.member.post'
    _description = 'Bài viết của hội viên'
    _rec_name = 'title'
    _order = 'publish_date desc, id desc'

    member_id = fields.Many2one('eaut.member', 'Hội viên', required=True, ondelete='cascade', index=True)
    title = fields.Char('Tiêu đề', required=True)
    cover = fields.Image('Ảnh đại diện', max_width=1024, max_height=1024)
    summary = fields.Text('Tóm tắt')
    content = fields.Html('Nội dung', sanitize_attributes=False)
    publish_date = fields.Date('Ngày đăng', default=fields.Date.context_today)
    is_published = fields.Boolean('Hiển thị', default=True)
    website_url = fields.Char('Website URL', compute='_compute_website_url')

    @api.depends('title', 'member_id')
    def _compute_website_url(self):
        for post in self:
            if post.id and post.member_id:
                post.website_url = '%s/bai-viet/%s' % (
                    post.member_id.website_url, self.env['ir.http']._slug(post))
            else:
                post.website_url = False