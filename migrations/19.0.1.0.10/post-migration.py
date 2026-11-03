from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    """Chuyển tên/chức danh người đại diện nhập tay cũ thành liên hệ (res.partner)."""
    cr.execute("""
        SELECT id, representative_name, representative_position FROM eaut_member
        WHERE representative_id IS NULL AND COALESCE(representative_name, '') != ''
    """)
    rows = cr.fetchall()
    if not rows:
        return
    env = api.Environment(cr, SUPERUSER_ID, {})
    Partner = env['res.partner']
    for member_id, name, position in rows:
        partner = Partner.search([('name', '=', name)], limit=1) or Partner.create({
            'name': name, 'function': position or False})
        cr.execute("UPDATE eaut_member SET representative_id = %s WHERE id = %s", (partner.id, member_id))
    env['eaut.member'].invalidate_model(['representative_id'])
    env['eaut.member'].search([])._refresh_default_contents()
