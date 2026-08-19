{
    "name": "Invoicing  - Portugal / Angola",
    "summary": """
        Module for common invoicing requirements between Portuguese and Angolan localizations""",
    "author": "ARXILEAD",
    "website": "https://www.arxi.pt",
    "category": "Accounting & Finance",
    "version": "1.41",
    "license": "OPL-1",
    # automatic_refs, tax_exemptions, restrict_update_company_info,
    # invoice_shipping_info and print_conf_copies were absorbed into this
    # module (see migrations/1.37/pre-merge_absorbed_modules.py).
    # contract_instance_checker (decisão 2026-07-08, "REAL dependency", licensing
    # enforcement for at_ws_communication) was deleted outright by Arxi's own
    # v19 certification bundle (commit 6e30f65, 2026-08-13) with no replacement
    # module and no surviving code anywhere in this repo referencing it — the
    # enforcement it provided no longer exists in the delivered codebase either
    # way. Removed 2026-08-18 as a dangling depend on a module that doesn't
    # exist; not a policy decision to bypass licensing, since there is nothing
    # left to bypass. Flag to Arxi if licensing enforcement needs restoring.
    # "sale" added 2026-08-19: models/account_move.py declares
    # downpayment_origin = fields.Many2one('sale.order', ...) (present since
    # Arxi's v19 certification bundle, commit 6e30f65, 2026-08-13 — file size
    # ~doubled in that commit vs. the prior upload, consistent with fields
    # absorbed from l10n_pt_ao_sale without the manifest depend following).
    # Without this depend, module load order isn't guaranteed to have 'sale'
    # registered yet when this module's account.move fields are set up,
    # crashing with AssertionError: unknown comodel_name 'sale.order'.
    # l10n_pt_ao_sale already depends on sale_management (-> sale) and
    # defines the same field name on the same model, so this is a genuine
    # missing depend, not new coupling.
    "depends": [
        "account",
        "base_vat",
        "auth_password_policy_signup",
        "sale",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/res_groups.xml",
        "data/config_param.xml",
        "data/automatic_refs_config_param.xml",
        "data/payment_mechanism_data.xml",
        "report/report_templates.xml",
        "report/account_move_templates.xml",
        "report/account_payment_templates.xml",
        "report/report_warning.xml",
        "views/res_partner_views.xml",
        "views/product_template_views.xml",
        "views/res_company_views.xml",
        "views/account_journal_views.xml",
        "views/account_move_reason_views.xml",
        "views/account_cancel_wizard_views.xml",
        "views/account_move_views.xml",
        "views/account_move_download_zip_views.xml",
        "views/account_payment_views.xml",
        "views/account_document_type_views.xml",
        "views/account_move_reversal_view.xml",
        "views/payment_mechanism_views.xml",
        "views/tax_report_refund_type_views.xml",
        "views/res_config_settings_views.xml",
        "views/l10n_pt_ao_menus.xml",
        "views/account_account.xml",
        "views/ir_actions_report_views.xml",
        "wizard/warning_wizard_views.xml",
        # Absorbed satellite modules (Bloco C da migração v19) — the inherited
        # views were merged into the core view files above; only the new-model
        # views and the standalone display template remain as own files
        "views/account_tax_exemption_views.xml",
        "report/print_copies_display_templates.xml",
        # Bloco D: certified report protection (must load after the templates)
        "data/protected_reports_data.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "l10n_pt_ao/static/src/**/*",
        ],
        "web.report_assets_common": [
            "l10n_pt_ao/static/src/scss/reports.scss",
        ],
    },
    "application": True,
    "post_init_hook": "post_init_hook",
}
