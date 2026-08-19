import logging

_logger = logging.getLogger(__name__)


def _delete_view_and_inherited_children(cr, module, name):
    """Delete a view (by its xmlid) together with any views that inherit
    from it (directly or transitively), plus their ir_model_data entries.

    Needed because a plain ``DELETE FROM ir_ui_view WHERE id IN (...)``
    violates ``ir_ui_view_inherit_id_fkey`` when another view still has
    ``inherit_id`` pointing at the row being removed (confirmed
    2026-08-19, admincore: report_custom_invoice_document still had
    casperventures.override_narration_custom_report inheriting from it).
    """
    cr.execute(
        """
        WITH RECURSIVE view_tree AS (
            SELECT id FROM ir_ui_view
            WHERE id = (
                SELECT res_id FROM ir_model_data
                WHERE module = %s AND name = %s AND model = 'ir.ui.view'
            )
            UNION ALL
            SELECT v.id FROM ir_ui_view v
            JOIN view_tree vt ON v.inherit_id = vt.id
        )
        SELECT id FROM view_tree
        """,
        (module, name),
    )
    ids = [row[0] for row in cr.fetchall()]
    if not ids:
        return

    cr.execute("DELETE FROM ir_ui_view WHERE id = ANY(%s)", (ids,))
    _logger.info(f"Deleted {cr.rowcount} view(s) (incl. inherited children) for {module}.{name}")

    cr.execute(
        "DELETE FROM ir_model_data WHERE model = 'ir.ui.view' AND res_id = ANY(%s)",
        (ids,),
    )
    _logger.info(f"Deleted {cr.rowcount} external ID record(s) for {module}.{name} and its children")


def migrate(cr, version):
    """
    Remove old views before module update:
    - l10n_pt_ao_view_account_list
    - report_custom_invoice_document
    - view_account_form
    These views need to be removed to ensure proper update.
    """
    _logger.info("Running l10n_pt_ao pre-migration: removing old views")

    for view_name in (
        "l10n_pt_ao_view_account_list",
        "report_custom_invoice_document",
        "view_account_form",
    ):
        _delete_view_and_inherited_children(cr, "l10n_pt_ao", view_name)

    _logger.info("Finished l10n_pt_ao pre-migration")
