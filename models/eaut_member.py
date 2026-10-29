import calendar
import logging
from markupsafe import Markup, escape

from odoo import api, fields, models ,_

_logger = logging.getLogger(__name__)

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

    founding_date = fields.Date(
        'Ngày thành lập', tracking=True,
        help='Hằng năm, đúng ngày này hệ thống tự gửi email chúc mừng kỷ niệm đến email của hội viên.')
    last_anniversary_year = fields.Integer(
        'Năm đã gửi email chúc mừng gần nhất', copy=False, readonly=True,
        help='Dùng để không gửi trùng trong cùng một năm.')

    product_ids = fields.One2many('eaut.member.product', 'member_id', 'Sản phẩm')
    service_ids = fields.One2many('eaut.member.service', 'member_id', 'Dịch vụ')
    post_ids = fields.One2many('eaut.member.post', 'member_id', 'Bài viết')
    gallery_ids = fields.One2many('eaut.member.gallery', 'member_id', 'Thư viện ảnh')
    contact_request_ids = fields.One2many('eaut.member.contact.request', 'member_id', 'Yêu cầu liên hệ')

    stat_ids = fields.One2many('eaut.member.stat', 'member_id', 'Số liệu nổi bật')
    award_ids = fields.One2many('eaut.member.award', 'member_id', 'Chứng nhận / Giải thưởng')
    hero_customized = fields.Boolean('Đã chỉnh nội dung đầu trang trên website', copy=False)
    card_customized = fields.Boolean('Đã chỉnh nội dung thẻ trên website', copy=False)
    contact_customized = fields.Boolean('Đã chỉnh khối liên hệ trên website', copy=False)
    stats_customized = fields.Boolean('Đã chỉnh khối số liệu trên website', copy=False)
    stats_content = fields.Html(
        'Khối số liệu nổi bật', sanitize_attributes=False,
        help='Giá trị và nhãn số liệu hiển thị ở tab Tổng quan. Chỉnh trực tiếp trên website (font, cỡ chữ, màu...).')
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

    def _default_stats_content(self):
        self.ensure_one()
        if not self.stat_ids:
            return False
        items = Markup('').join(
            Markup(
                '<div class="col-12 col-sm-6"><div class="d-flex align-items-center gap-3">'
                '<span class="eaut-stat-icon"><i class="fa %s"></i></span>'
                '<div><div class="eaut-stat-value">%s</div><div class="eaut-stat-label">%s</div></div>'
                '</div></div>'
            ) % (stat.icon or 'fa-star', escape(stat.value or ''), escape(stat.name or ''))
            for stat in self.stat_ids)
        return Markup('<div class="row g-3 eaut-stats">%s</div>') % items

    # Khối Html (hero/card/contact/stats) được sinh từ thông tin của hội viên. Khối nào chưa bị
    # chỉnh tay trên website thì tự sinh lại khi thông tin gốc đổi; khối đã chỉnh thì được giữ nguyên.
    _CONTENT_FLAGS = {
        'hero_content': 'hero_customized',
        'card_content': 'card_customized',
        'contact_content': 'contact_customized',
        'stats_content': 'stats_customized',
    }
    _CONTENT_SOURCE_FIELDS = {
        'name', 'short_description', 'representative_name', 'representative_position',
        'industry_id', 'phone', 'email', 'website', 'address',
    }

    def _refresh_default_contents(self, force=False):
        """Sinh lại các khối nội dung mặc định.

        Khối đã được chỉnh trên website được giữ nguyên, trừ khi force=True
        (khi đó sinh lại tất cả và bỏ đánh dấu đã chỉnh).
        """
        for member in self.with_context(eaut_auto_content=True):
            vals = {}
            if force or not member.hero_customized:
                vals['hero_content'] = member._default_hero_content()
            if force or not member.card_customized:
                vals['card_content'] = member._default_card_content()
            if force or not member.contact_customized:
                vals['contact_content'] = member._default_contact_content()
            if force or not member.stats_customized:
                vals['stats_content'] = member._default_stats_content()
            if force:
                vals.update({flag: False for flag in self._CONTENT_FLAGS.values()})
            if vals:
                member.write(vals)

    def _refresh_stats_content(self):
        for member in self.with_context(eaut_auto_content=True):
            if not member.stats_customized:
                member.write({'stats_content': member._default_stats_content()})

    def action_rebuild_contents(self):
        """Tạo lại toàn bộ nội dung từ thông tin hội viên (mất các chỉnh sửa định dạng trên website)."""
        self._refresh_default_contents(force=True)

    def action_rebuild_stats_content(self):
        """Tạo lại khối số liệu từ danh sách (mất các chỉnh sửa định dạng trên website)."""
        for member in self.with_context(eaut_auto_content=True):
            member.write({
                'stats_content': member._default_stats_content(),
                'stats_customized': False,
            })

    @api.model_create_multi
    def create(self, vals_list):
        members = super().create(vals_list)
        for member, vals in zip(members, vals_list):
            # nội dung được truyền sẵn khi tạo (ví dụ import) coi như đã chỉnh tay
            flags = {flag: True for field, flag in self._CONTENT_FLAGS.items() if vals.get(field)}
            if flags:
                member.with_context(eaut_auto_content=True).write(flags)
        members._refresh_default_contents()
        return members

    def write(self, vals):
        if self.env.context.get('eaut_auto_content'):
            return super().write(vals)
        vals = dict(vals)
        for field, flag in self._CONTENT_FLAGS.items():
            if field in vals:
                vals.setdefault(flag, True)  # ghi trực tiếp (ví dụ từ website builder) = đã chỉnh tay
        res = super().write(vals)
        if self._CONTENT_SOURCE_FIELDS & vals.keys():
            self._refresh_default_contents()
        return res

    def get_anniversary_years(self):
        """Số năm thành lập tính đến năm hiện tại (dùng trong mẫu email)."""
        self.ensure_one()
        if not self.founding_date:
            return 0
        return fields.Date.context_today(self).year - self.founding_date.year

    @api.model
    def _is_founding_anniversary(self, founding_date, today):
        if (founding_date.month, founding_date.day) == (today.month, today.day):
            return True
        # Thành lập ngày 29/2: năm không nhuận thì chúc mừng vào 28/2
        return (
                (founding_date.month, founding_date.day) == (2, 29)
                and (today.month, today.day) == (2, 28)
                and not calendar.isleap(today.year)
        )

    def _send_anniversary_email(self):
        """Gửi email chúc mừng kỷ niệm thành lập, ghi chatter và đánh dấu đã gửi trong năm."""
        self.ensure_one()
        today = fields.Date.context_today(self)
        if not self.founding_date or self.founding_date.year >= today.year:
            return 'no_date'
        if self.last_anniversary_year == today.year:
            return 'duplicate'
        template = self.env.ref(
            'eaut_member_customize.mail_template_founding_anniversary', raise_if_not_found=False)
        if not template:
            return 'no_template'
        if not (self.email or self.partner_id.email):
            return 'no_email'
        template.send_mail(self.id, force_send=False)
        self.last_anniversary_year = today.year
        self.message_post(
            body=_('Đã gửi email chúc mừng kỷ niệm %s năm thành lập.', self.get_anniversary_years()),
            subtype_xmlid='mail.mt_note')
        return 'sent'

    @api.model
    def _cron_send_anniversary_emails(self):
        """Chạy hằng ngày: gửi email chúc mừng cho hội viên có kỷ niệm thành lập hôm nay."""
        today = fields.Date.context_today(self)
        members = self.search([
            ('founding_date', '!=', False),
            ('last_anniversary_year', '!=', today.year),
        ])
        for member in members:
            if not self._is_founding_anniversary(member.founding_date, today):
                continue
            try:
                result = member._send_anniversary_email()
                if result not in ('sent', 'no_date'):
                    _logger.info('Bỏ qua chúc mừng hội viên %s: %s', member.id, result)
            except Exception:
                _logger.exception('Không gửi được email chúc mừng cho hội viên %s', member.id)

    def action_send_anniversary_email(self):
        """Nút trên form: gửi email chúc mừng ngay; chặn gửi trùng trong cùng một năm."""
        results = [member._send_anniversary_email() for member in self]
        sent = results.count('sent')
        if sent:
            message = _('Đã đưa %s email chúc mừng vào hàng đợi gửi.', sent)
            kind = 'success'
        elif 'duplicate' in results:
            message = _('Năm nay đã gửi email chúc mừng cho hội viên này, không gửi lại.')
            kind = 'warning'
        elif 'no_email' in results:
            message = _('Chưa gửi: hội viên chưa có email (hoặc email của liên hệ liên kết).')
            kind = 'warning'
        elif 'no_template' in results:
            message = _('Chưa gửi: không tìm thấy mẫu email chúc mừng.')
            kind = 'danger'
        else:
            message = _('Chưa gửi: hội viên cần có ngày thành lập trước năm hiện tại.')
            kind = 'warning'
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {'title': _('Email chúc mừng'), 'message': message, 'type': kind, 'sticky': False},
        }


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

    @api.model_create_multi
    def create(self, vals_list):
        stats = super().create(vals_list)
        stats.member_id._refresh_stats_content()
        return stats

    def write(self, vals):
        members = self.member_id
        res = super().write(vals)
        (members | self.member_id)._refresh_stats_content()
        return res

    def unlink(self):
        members = self.member_id
        res = super().unlink()
        members._refresh_stats_content()
        return res


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