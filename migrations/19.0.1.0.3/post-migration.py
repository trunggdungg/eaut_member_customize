from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    """Điền sẵn nội dung thẻ danh sách (chỉnh style được trên website) cho hội viên cũ."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    for member in env['eaut.member'].with_context(active_test=False).search([('card_content', '=', False)]):
        member.card_content = member._default_card_content()