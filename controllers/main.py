from odoo import http
from odoo.http import request

MEMBER_TABS = [
    ('tong-quan', 'Tổng quan'),
    ('san-pham', 'Sản phẩm'),
    ('dich-vu', 'Dịch vụ'),
    ('bai-viet', 'Bài viết'),
    ('thu-vien', 'Thư viện ảnh'),
    ('lien-he', 'Liên hệ'),
]

MEMBER_SORTS = {
    'default': ('Mặc định', 'sequence asc, id asc'),
    'name': ('Tên A-Z', 'name asc'),
    'newest': ('Mới nhất', 'join_date desc, id desc'),
}


class EautMemberController(http.Controller):
    _per_page = 12

    @http.route(['/hoi-vien', '/hoi-vien/page/<int:page>'], type='http', auth='public',
                website=True, sitemap=True)
    def members(self, page=1, industry=None, search='', order='default', **kw):
        Member = request.env['eaut.member']
        domain = [('website_published', '=', True)]
        url_args = {}

        industry_id = int(industry) if industry and str(industry).isdigit() else False
        if industry_id:
            domain.append(('industry_id', '=', industry_id))
            url_args['industry'] = industry_id
        if search:
            domain += ['|', ('name', 'ilike', search), ('representative_name', 'ilike', search)]
            url_args['search'] = search
        if order not in MEMBER_SORTS:
            order = 'default'
        if order != 'default':
            url_args['order'] = order

        total = Member.search_count(domain)
        pager = request.website.pager(
            url='/hoi-vien', total=total, page=page, step=self._per_page,
            scope=5, url_args=url_args)
        members = Member.search(
            domain, order=MEMBER_SORTS[order][1],
            limit=self._per_page, offset=pager['offset'])

        return request.render('eaut_member_customize.members_page', {
            'members': members,
            'total': total,
            'pager': pager,
            'industries': request.env['eaut.member.industry'].search([]),
            'industry_id': industry_id,
            'search': search,
            'order': order,
            'sorts': MEMBER_SORTS,
        })

    @http.route([
        '/hoi-vien/<model("eaut.member"):member>',
        '/hoi-vien/<model("eaut.member"):member>/<string:tab>',
    ], type='http', auth='public', website=True, sitemap=False)
    def member_detail(self, member, tab='tong-quan', q='', sent=None, **kw):
        if tab not in dict(MEMBER_TABS):
            raise request.not_found()
        values = {
            'member': member,
            'tab': tab,
            'tabs': MEMBER_TABS,
            'q': q,
            'sent': bool(sent),
        }
        if tab == 'san-pham':
            domain = [('member_id', '=', member.id), ('is_published', '=', True)]
            if q:
                domain.append(('name', 'ilike', q))
            values['products'] = request.env['eaut.member.product'].search(domain)
        elif tab == 'dich-vu':
            values['services'] = request.env['eaut.member.service'].search(
                [('member_id', '=', member.id), ('is_published', '=', True)])
        elif tab == 'bai-viet':
            values['posts'] = request.env['eaut.member.post'].search(
                [('member_id', '=', member.id), ('is_published', '=', True)])
        elif tab == 'thu-vien':
            values['gallery'] = request.env['eaut.member.gallery'].search(
                [('member_id', '=', member.id), ('is_published', '=', True)])
        return request.render('eaut_member_customize.member_detail_page', values)

    @http.route('/hoi-vien/<model("eaut.member"):member>/bai-viet/<model("eaut.member.post"):post>',
                type='http', auth='public', website=True, sitemap=False)
    def member_post(self, member, post, **kw):
        if post.member_id != member:
            raise request.not_found()
        return request.render('eaut_member_customize.member_post_page', {
            'member': member,
            'post': post,
            'tab': 'bai-viet',
            'tabs': MEMBER_TABS,
        })

    @http.route('/hoi-vien/<model("eaut.member"):member>/lien-he/gui', type='http',
                auth='public', website=True, methods=['POST'], csrf=True, sitemap=False)
    def member_contact_submit(self, member, **post):
        name = (post.get('name') or '').strip()
        email = (post.get('email') or '').strip()
        phone = (post.get('phone') or '').strip()
        if name and (email or phone):
            request.env['eaut.member.contact.request'].sudo().create({
                'member_id': member.id,
                'name': name,
                'email': email,
                'phone': phone,
                'message': (post.get('message') or '').strip(),
            })
            return request.redirect('%s/lien-he?sent=1' % member.website_url)
        return request.redirect('%s/lien-he' % member.website_url)
