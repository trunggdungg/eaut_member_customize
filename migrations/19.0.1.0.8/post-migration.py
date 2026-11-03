def migrate(cr, version):
    # hội viên đang xuất bản trước khi có giai đoạn được coi là đã là "Hội viên"
    cr.execute("UPDATE eaut_member SET stage = 'member' WHERE website_published")
