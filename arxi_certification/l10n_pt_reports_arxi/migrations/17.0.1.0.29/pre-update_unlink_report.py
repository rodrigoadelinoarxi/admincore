from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    if report := env.ref('l10n_pt_reports_arxi.tax_report_pt_anexo_clientes'):
        report.unlink()
    if report := env.ref('l10n_pt_reports_arxi.tax_report_pt_anexo_fornecedores'):
        report.unlink()
    if report := env.ref('l10n_pt_reports_arxi.tax_report_pt_anexo_40'):
        report.unlink()
    if report := env.ref('l10n_pt_reports_arxi.tax_report_pt_anexo_41'):
        report.unlink()