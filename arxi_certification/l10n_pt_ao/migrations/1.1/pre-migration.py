import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """
    Remove old views before module update:
    - l10n_pt_ao_view_account_list
    - report_custom_invoice_document
    - view_account_form
    These views need to be removed to ensure proper update.
    """
    _logger.info("Running l10n_pt_ao pre-migration: removing old views")

    # Delete the old account list view if it exists
    cr.execute("""
        DELETE FROM ir_ui_view
        WHERE id IN (
            SELECT res_id FROM ir_model_data
            WHERE module = 'l10n_pt_ao'
            AND name = 'l10n_pt_ao_view_account_list'
            AND model = 'ir.ui.view'
        )
    """)

    deleted_views = cr.rowcount
    if deleted_views > 0:
        _logger.info(f"Deleted {deleted_views} l10n_pt_ao_view_account_list view(s)")

    # Delete the external ID record
    cr.execute("""
        DELETE FROM ir_model_data
        WHERE module = 'l10n_pt_ao'
        AND name = 'l10n_pt_ao_view_account_list'
        AND model = 'ir.ui.view'
    """)

    deleted_ids = cr.rowcount
    if deleted_ids > 0:
        _logger.info(f"Deleted {deleted_ids} external ID record(s) for l10n_pt_ao_view_account_list")

    # Delete the old report_custom_invoice_document view if it exists
    cr.execute("""
        DELETE FROM ir_ui_view
        WHERE id IN (
            SELECT res_id FROM ir_model_data
            WHERE module = 'l10n_pt_ao'
            AND name = 'report_custom_invoice_document'
            AND model = 'ir.ui.view'
        )
    """)

    deleted_views = cr.rowcount
    if deleted_views > 0:
        _logger.info(f"Deleted {deleted_views} report_custom_invoice_document view(s)")

    # Delete the external ID record
    cr.execute("""
        DELETE FROM ir_model_data
        WHERE module = 'l10n_pt_ao'
        AND name = 'report_custom_invoice_document'
        AND model = 'ir.ui.view'
    """)

    deleted_ids = cr.rowcount
    if deleted_ids > 0:
        _logger.info(f"Deleted {deleted_ids} external ID record(s) for report_custom_invoice_document")

    # Delete the old view_account_form view if it exists
    cr.execute("""
        DELETE FROM ir_ui_view
        WHERE id IN (
            SELECT res_id FROM ir_model_data
            WHERE module = 'l10n_pt_ao'
            AND name = 'view_account_form'
            AND model = 'ir.ui.view'
        )
    """)

    deleted_views = cr.rowcount
    if deleted_views > 0:
        _logger.info(f"Deleted {deleted_views} view_account_form view(s)")

    # Delete the external ID record
    cr.execute("""
        DELETE FROM ir_model_data
        WHERE module = 'l10n_pt_ao'
        AND name = 'view_account_form'
        AND model = 'ir.ui.view'
    """)

    deleted_ids = cr.rowcount
    if deleted_ids > 0:
        _logger.info(f"Deleted {deleted_ids} external ID record(s) for view_account_form")

    _logger.info("Finished l10n_pt_ao pre-migration")
