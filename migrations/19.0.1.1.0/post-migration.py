from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    """Đồng bộ một lần các khối nội dung đã cũ (chụp lúc tạo) theo thông tin hiện tại của hội viên."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    members = env['eaut.member'].with_context(active_test=False).search([])
    members._refresh_default_contents(force=True)
