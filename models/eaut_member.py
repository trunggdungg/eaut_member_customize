from odoo import api, fields, models


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


class EautMember(models.Model):
    _name = 'eaut.member'
    _description = 'Hội viên'
    _inherit = ['mail.thread', 'website.published.mixin', 'website.seo.metadata']
    _order = 'sequence, id'

    name = fields.Char('Tên công ty', required=True, tracking=True, index=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    logo = fields.Image('Logo', max_width=512, max_height=512)
    banner = fields.Image('Ảnh bìa', max_width=1920, max_height=600)
    industry_id = fields.Many2one('eaut.member.industry', 'Ngành nghề', tracking=True)
    short_description = fields.Text('Mô tả ngắn')
    description = fields.Html('Giới thiệu', sanitize_attributes=False)
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


class EautMemberProduct(models.Model):
    _name = 'eaut.member.product'
    _description = 'Sản phẩm của hội viên'
    _order = 'sequence, id'

    member_id = fields.Many2one('eaut.member', 'Hội viên', required=True, ondelete='cascade', index=True)
    name = fields.Char('Tên sản phẩm', required=True)
    sequence = fields.Integer(default=10)
    image = fields.Image('Hình ảnh', max_width=1024, max_height=1024)
    description = fields.Text('Mô tả')
    is_published = fields.Boolean('Hiển thị', default=True)


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


class EautMemberGallery(models.Model):
    _name = 'eaut.member.gallery'
    _description = 'Thư viện ảnh của hội viên'
    _order = 'sequence, id'

    member_id = fields.Many2one('eaut.member', 'Hội viên', required=True, ondelete='cascade', index=True)
    name = fields.Char('Chú thích')
    sequence = fields.Integer(default=10)
    image = fields.Image('Hình ảnh', required=True, max_width=1920, max_height=1920)
    is_published = fields.Boolean('Hiển thị', default=True)


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


class EautMemberContactRequest(models.Model):
    _name = 'eaut.member.contact.request'
    _description = 'Yêu cầu liên hệ hội viên'
    _order = 'id desc'

    member_id = fields.Many2one('eaut.member', 'Hội viên', required=True, ondelete='cascade', index=True)
    name = fields.Char('Họ tên', required=True)
    email = fields.Char('Email')
    phone = fields.Char('Điện thoại')
    message = fields.Text('Nội dung')
