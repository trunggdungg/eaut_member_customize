{
    'name': 'Hội viên (EAUT)',
    'version': '19.0.1.1.0',
    'category': 'Website',
    'summary': 'Quản lý hội viên và hiển thị hồ sơ hội viên (sản phẩm, dịch vụ, bài viết, thư viện ảnh) trên website',
    'depends': ['base', 'mail', 'website'],
    'data': [
        'security/eaut_member_groups.xml',
        'security/ir.model.access.csv',
        'security/eaut_member_rules.xml',
        'views/eaut_contact_views.xml',
        'data/eaut_contact_form_data.xml',
        'data/eaut_member_data.xml',
        'views/eaut_member_views.xml',
        'data/eaut_member_mail_data.xml',
        'views/eaut_member_menus.xml',
        'views/website_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'eaut_member_customize/static/src/scss/eaut_member.scss',
        ],
        'website.assets_wysiwyg': [
            'eaut_member_customize/static/src/js/eaut_contact_form.js',
        ],
        'website.website_builder_assets': [
            'eaut_member_customize/static/src/js/eaut_contact_form.js',
        ],
    },
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}
