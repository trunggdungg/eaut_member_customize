# eaut_member_customize – Quản lý hội viên (Odoo 19 Community)

Module dùng chung để quản lý hội viên/doanh nghiệp thành viên và hiển thị hồ sơ lên website
(sản phẩm, dịch vụ, bài viết, thư viện ảnh, liên hệ). Có thể tái sử dụng cho nhiều dự án.

## Cài đặt
1. Copy thư mục `eaut_member_customize` vào thư mục addons.
2. Restart Odoo, bật chế độ nhà phát triển, Apps > Update Apps List.
3. Tìm "Hội viên (EAUT)" và cài đặt.

## Sử dụng
- Menu **Hội viên**: nhập hội viên, ngành nghề, sản phẩm, dịch vụ, bài viết, thư viện ảnh.
- Bật nút **Xuất bản** trên form hội viên để hiển thị ra web.
- Website: `/hoi-vien` (danh sách), `/hoi-vien/<slug>` (chi tiết, các tab).
- Yêu cầu liên hệ gửi từ web được lưu ở menu **Yêu cầu liên hệ**.

## Models
`eaut.member`, `eaut.member.industry`, `eaut.member.product`, `eaut.member.service`,
`eaut.member.gallery`, `eaut.member.post`, `eaut.member.contact.request`.
