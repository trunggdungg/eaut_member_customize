import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";

// Các ô mặc định khi chọn Tác vụ "Gửi liên hệ về app Hội viên" trong website builder.
// `force` vì file có thể được nạp ở nhiều bundle của website builder.
registry.category("website.form_editor_actions").add("eaut_contact", {
    formFields: [
        {
            type: "char",
            modelRequired: true,
            name: "name",
            string: _t("Họ tên"),
        },
        {
            type: "email",
            name: "email",
            string: _t("Email"),
        },
        {
            type: "tel",
            name: "phone",
            string: _t("Điện thoại"),
        },
        {
            type: "char",
            name: "subject",
            string: _t("Tiêu đề"),
        },
        {
            type: "text",
            name: "message",
            string: _t("Nội dung"),
        },
    ],
}, { force: true });