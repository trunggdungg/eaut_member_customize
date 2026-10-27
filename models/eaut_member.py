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
    contact_content = fields.Html(
        'Khối thông tin liên hệ', sanitize_attributes=False,
        help='Thông tin hiển thị ở cột phải trang hội viên. Chỉnh trực tiếp trên website (font, cỡ chữ, màu...).')
    hero_content = fields.Html(
        'Nội dung đầu trang', sanitize_attributes=False,
        help='Chữ hiển thị trên ảnh bìa. Chỉnh trực tiếp trên website (font, cỡ chữ, màu...).')
    card_content = fields.Html(
        'Nội dung thẻ danh sách', sanitize_attributes=False,
        help='Tên, người đại diện và ngành nghề hiển thị trên thẻ ở trang danh sách. Chỉnh trực tiếp trên website.')
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

    stat_ids = fields.One2many('eaut.member.stat', 'member_id', 'Số liệu nổi bật')
    award_ids = fields.One2many('eaut.member.award', 'member_id', 'Chứng nhận / Giải thưởng')

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

    def _default_card_content(self):
        self.ensure_one()
        parts = [Markup('<h5 class="eaut-card-name">%s</h5>') % escape(self.name or '')]
        if self.representative_name:
            text = escape(self.representative_name)
            if self.representative_position:
                text = Markup('%s / %s') % (text, escape(self.representative_position))
            parts.append(Markup('<div class="eaut-badge">%s</div>') % text)
        if self.industry_id:
            parts.append(Markup('<div class="eaut-card-industry text-muted">%s</div>') % escape(self.industry_id.name))
        return Markup('').join(parts)

    def _default_contact_content(self):
        self.ensure_one()
        rows = []
        if self.industry_id:
            rows.append(('fa-industry', escape(self.industry_id.name)))
        if self.representative_name:
            text = escape(self.representative_name)
            if self.representative_position:
                text = Markup('%s - %s') % (text, escape(self.representative_position))
            rows.append(('fa-user', text))
        if self.address:
            rows.append(('fa-map-marker', escape(self.address)))
        if self.phone:
            rows.append(('fa-phone', escape(self.phone)))
        if self.email:
            rows.append(('fa-envelope', Markup('<a href="mailto:%s">%s</a>') % (
                escape(self.email), escape(self.email))))
        if self.website:
            rows.append(('fa-globe', Markup('<a href="%s" target="_blank" rel="noopener">%s</a>') % (
                escape(self.website), escape(self.website))))
        return Markup('').join(
            Markup('<p><i class="fa %s fa-fw"></i> %s</p>') % (icon, text) for icon, text in rows)

    @api.model
    def _fill_default_contents(self):
        """Điền nội dung mặc định cho hội viên chưa có (chạy mỗi lần cài/nâng cấp module)."""
        for member in self.with_context(active_test=False).search([]):
            vals = {}
            if not member.hero_content:
                vals['hero_content'] = member._default_hero_content()
            if not member.card_content:
                vals['card_content'] = member._default_card_content()
            if not member.contact_content:
                vals['contact_content'] = member._default_contact_content()
            if vals:
                member.write(vals)


    @api.model_create_multi
    def create(self, vals_list):
        members = super().create(vals_list)
        for member in members.filtered(lambda m: not m.hero_content):
            member.hero_content = member._default_hero_content()
        for member in members.filtered(lambda m: not m.card_content):
            member.card_content = member._default_card_content()
        for member in members.filtered(lambda m: not m.contact_content):
            member.contact_content = member._default_contact_content()
        return members

    def action_publish(self):
        self.write({'website_published': True})

    def action_unpublish(self):
        self.write({'website_published': False})



STAT_ICONS = [
    ('fa-star', 'Ngôi sao'),
    ('fa-bullseye', 'Mục tiêu'),
    ('fa-calendar', 'Lịch (năm thành lập)'),
    ('fa-industry', 'Nhà máy'),
    ('fa-globe', 'Quốc gia / thị trường'),
    ('fa-users', 'Nhân sự'),
    ('fa-building', 'Công ty / chi nhánh'),
    ('fa-briefcase', 'Dự án / hợp đồng'),
    ('fa-line-chart', 'Doanh thu / tăng trưởng'),
    ('fa-trophy', 'Cúp'),
    ('fa-handshake-o', 'Đối tác'),
    ('fa-certificate', 'Chứng chỉ'),
]


class EautMemberStat(models.Model):
    _name = 'eaut.member.stat'
    _description = 'Số liệu nổi bật của hội viên'
    _order = 'sequence, id'

    member_id = fields.Many2one('eaut.member', 'Hội viên', required=True, ondelete='cascade', index=True)
    sequence = fields.Integer(default=10)
    icon = fields.Selection(STAT_ICONS, 'Biểu tượng', default='fa-star', required=True)
    value = fields.Char('Giá trị', required=True, help='Ví dụ: 28, 10+, 2000+')
    name = fields.Char('Nhãn', required=True, help='Ví dụ: Số năm thành lập, Nhà máy')


class EautMemberAward(models.Model):
    _name = 'eaut.member.award'
    _description = 'Chứng nhận / giải thưởng của hội viên'
    _order = 'sequence, id'

    member_id = fields.Many2one('eaut.member', 'Hội viên', required=True, ondelete='cascade', index=True)
    sequence = fields.Integer(default=10)
    award_type = fields.Char('Loại', default='Chứng nhận', help='Ví dụ: Chứng nhận, Giải thưởng, Huy chương')
    name = fields.Char('Tên chứng nhận / giải thưởng', required=True)
    year = fields.Char('Năm')
    image = fields.Image('Hình ảnh', max_width=512, max_height=512,
                         help='Để trống sẽ hiển thị biểu tượng mặc định.')