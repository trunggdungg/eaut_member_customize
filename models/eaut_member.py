from markupsafe import Markup, escape

from odoo import api, fields, models


class EautMember(models.Model):
    _name = 'eaut.member'
    _description = 'Hội viên'
    _inherit = ['mail.thread', 'website.published.mixin', 'website.seo.metadata',
                'website.cover_properties.mixin']
    _order = 'sequence, id'

    name = fields.Char('Tên công ty', required=True, tracking=True, index=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    logo = fields.Image('Logo', max_width=512, max_height=512)
    banner = fields.Image('Ảnh bìa', max_width=1920, max_height=600)
    industry_id = fields.Many2one('eaut.member.industry', 'Ngành nghề', tracking=True)
    short_description = fields.Text('Mô tả ngắn')
    description = fields.Html('Giới thiệu', sanitize_attributes=False)
    hero_content = fields.Html(
        'Nội dung đầu trang', sanitize_attributes=False,
        help='Chữ hiển thị trên ảnh bìa. Chỉnh trực tiếp trên website (font, cỡ chữ, màu...).')
    representative_name = fields.Char('Người đại diện')
    representative_position = fields.Char('Chức danh')
    phone = fields.Char('Điện thoại')
    email = fields.Char('Email')
    website = fields.Char('Website')
    address = fields.Char('Địa chỉ')
    join_date = fields.Date('Ngày gia nhập')
    partner_id = fields.Many2one('res.partner', 'Liên hệ liên kết')

    product_ids = fields.One2many('eaut.member.product', 'member_id', 'Sản phẩm')
    service_ids = fields.One2many('eaut.member.service', 'member_id', 'Dịch vụ')
    post_ids = fields.One2many('eaut.member.post', 'member_id', 'Bài viết')
    gallery_ids = fields.One2many('eaut.member.gallery', 'member_id', 'Thư viện ảnh')
    contact_request_ids = fields.One2many('eaut.member.contact.request', 'member_id', 'Yêu cầu liên hệ')

    @api.depends('name')
    def _compute_website_url(self):
        super()._compute_website_url()
        for member in self:
            if member.id:
                member.website_url = '/hoi-vien/%s' % self.env['ir.http']._slug(member)

    def _default_hero_content(self):
        self.ensure_one()
        return Markup(
            '<p class="eaut-hero-label">HỘI VIÊN</p>'
            '<h1 class="eaut-hero-title">%s</h1>'
            '<p class="eaut-hero-desc">%s</p>'
        ) % (escape(self.name or ''), escape(self.short_description or ''))

    @api.model_create_multi
    def create(self, vals_list):
        members = super().create(vals_list)
        for member in members.filtered(lambda m: not m.hero_content):
            member.hero_content = member._default_hero_content()
        return members

    def action_publish(self):
        self.write({'website_published': True})

    def action_unpublish(self):
        self.write({'website_published': False})