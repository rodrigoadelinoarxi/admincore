# -*- coding: utf-8 -*-
"""Merge the absorbed satellite modules into l10n_pt_ao (Bloco C, migração v19).

Old databases have these modules installed as standalone apps. Their code now
lives inside l10n_pt_ao, so this pre-migration:

0. Deletes the satellites' inherited views/templates whose xpath specs were
   merged directly into the core view files (decisão do técnico: as vistas são
   absorvidas nas existentes, sem manter inherits paralelos) — see
   OBSOLETE_VIEWS. Leaving them would duplicate UI elements.
1. Re-parents every remaining ir_model_data entry (standalone views, menus,
   actions, access rules, config parameters, model/field metadata) from the
   old module to l10n_pt_ao — keeping the record `name`, which matches the
   xml_ids of the files moved into the core. On a name collision with an
   existing l10n_pt_ao entry, the record is renamed to ``<name>_<old_module>``
   (safety net; no known case after the view merge).
2. Marks the old module as uninstalled WITHOUT running the uninstall routine —
   the data must survive, it is now owned by l10n_pt_ao.
3. Drops stale dependency rows pointing at the merged modules so the upgrade
   of the remaining modules does not fail on "unmet dependency".

Idempotent: re-running finds nothing left to move.

Note: ir.config_parameter KEYS keep their historical names
(``automatic_refs.*``) on purpose — they are plain strings read by the core
code and renaming them would need a data migration with no benefit.
"""
import logging

_logger = logging.getLogger(__name__)

MERGED_MODULES = [
    'automatic_refs',
    'tax_exemptions',
    'invoice_shipping_info',
    'print_conf_copies',
    'restrict_update_company_info',
    'account_cancel_reason',
    'credit_note_reason',
    # replaced by the core protected-report mechanism (Bloco D), not merged:
    # its enforcement now lives in ir_actions_report.py/ir_ui_view.py
    'studio_protected_reports',
]

# Modules removed for good (Etapa 1 da migração v19) — unlike the merged ones
# their data must NOT survive: they are marked 'to remove' so Odoo runs a real
# uninstall during the upgrade cycle (views, fields and records cleaned up).
# contract_instance_checker is NOT here: it moved to the arxi-quality repo
# keeping the same module name, so installed DBs keep it running from the new
# location. Same reasoning for sale_force_invoiced: it is upstream OCA
# (ForgeFlow, sale-workflow) and was only being vendored here — dropping it from
# this repo does not uninstall it, so DBs that use it keep their force_invoiced
# data and serve the module from the OCA repo instead.
REMOVED_MODULES = [
    'sh_message',
    'sh_import_journal_entry',
    'credit_note_smart_button',
    'ir_rule_protected',
    'access_apps',
    'access_restricted',
    'restricted_settings',
]

# Models replaced by the unified account.move.reason: their registry metadata
# is removed (the code no longer defines them); the TABLE is kept untouched as
# a data safeguard — post-unify_move_reasons.py copies its rows.
DROPPED_MODELS = [
    'account.move.refund.reason',
]

# Window actions/menu entries pointing at dropped models — deleted instead of
# re-parented (they would stay broken).
OBSOLETE_ACTIONS = [
    ('credit_note_reason', 'account_move_refund_reason_action'),
]

# Inherited views/templates whose specs were merged INTO the core view files —
# these records must be DELETED in old databases (their xml_ids no longer
# exist), otherwise they would survive as orphan inherits duplicating the UI
# elements now provided by the core views.
OBSOLETE_VIEWS = [
    ('automatic_refs', 'res_config_settings_view_form'),
    ('automatic_refs', 'view_partner_form_automatic_ref'),
    ('invoice_shipping_info', 'view_move_form'),
    ('invoice_shipping_info', 'report_invoice_document'),
    ('print_conf_copies', 'view_company_form_print_conf_copies'),
    ('print_conf_copies', 'view_partner_form_print_conf_copies'),
    ('print_conf_copies', 'invoice_form_print_conf_copies'),
    ('print_conf_copies', 'view_account_payment_form_print_conf_copies'),
    ('print_conf_copies', 'print_copies_report_invoice'),
    ('print_conf_copies', 'print_copies_report_invoice_document'),
    ('print_conf_copies', 'report_payment_receipt_document'),
    ('account_cancel_reason', 'view_move_form'),
    ('account_cancel_reason', 'view_account_payment_form'),
    ('account_cancel_reason', 'report_invoice_account_cancel_reason'),
    ('account_cancel_reason', 'report_payment_inherit'),
    ('credit_note_reason', 'view_account_move_reversal'),
    ('credit_note_reason', 'account_move_refund_reason_view_tree'),
    ('credit_note_reason', 'account_move_refund_reason_view_search'),
]


def migrate(cr, version):
    """Re-parent the merged modules' metadata into l10n_pt_ao.

    :param cr: database cursor
    :param version: installed module version before the upgrade (None on
        fresh installs, where there is nothing to merge)
    """
    if not version:
        return

    # 0. drop the inherited views whose specs were merged into the core views
    for module, name in OBSOLETE_VIEWS:
        cr.execute(
            """
            DELETE FROM ir_ui_view v
             USING ir_model_data d
             WHERE d.module = %s AND d.name = %s
               AND d.model = 'ir.ui.view' AND v.id = d.res_id
            """,
            (module, name),
        )
        if cr.rowcount:
            _logger.info('l10n_pt_ao merge: dropped obsolete view %s.%s', module, name)
        cr.execute(
            "DELETE FROM ir_model_data WHERE module = %s AND name = %s AND model = 'ir.ui.view'",
            (module, name),
        )

    # 0a-bis. flag the removed modules for a REAL uninstall (data cleanup)
    cr.execute(
        """
        UPDATE ir_module_module
           SET state = 'to remove'
         WHERE name IN %s
           AND state = 'installed'
        """,
        (tuple(REMOVED_MODULES),),
    )
    if cr.rowcount:
        _logger.info('l10n_pt_ao cleanup: %s removed module(s) flagged for uninstall', cr.rowcount)

    # 0b. drop window actions pointing at dropped models
    for module, name in OBSOLETE_ACTIONS:
        cr.execute(
            """
            DELETE FROM ir_act_window a
             USING ir_model_data d
             WHERE d.module = %s AND d.name = %s
               AND d.model = 'ir.actions.act_window' AND a.id = d.res_id
            """,
            (module, name),
        )
        cr.execute(
            "DELETE FROM ir_model_data WHERE module = %s AND name = %s",
            (module, name),
        )

    # 0c. remove registry metadata of dropped models (tables stay as safeguard)
    for model in DROPPED_MODELS:
        cr.execute(
            """
            DELETE FROM ir_model_data
             WHERE (model = 'ir.model' AND res_id IN (SELECT id FROM ir_model WHERE model = %s))
                OR (model = 'ir.model.fields' AND res_id IN (SELECT id FROM ir_model_fields WHERE model = %s))
                OR (model = 'ir.model.fields.selection' AND res_id IN (
                        SELECT s.id FROM ir_model_fields_selection s
                        JOIN ir_model_fields f ON s.field_id = f.id WHERE f.model = %s))
            """,
            (model, model, model),
        )
        cr.execute(
            "DELETE FROM ir_model_fields_selection WHERE field_id IN (SELECT id FROM ir_model_fields WHERE model = %s)",
            (model,),
        )
        cr.execute("DELETE FROM ir_model_fields WHERE model = %s", (model,))
        cr.execute("DELETE FROM ir_model WHERE model = %s", (model,))
        _logger.info('l10n_pt_ao merge: dropped registry metadata of %s (table kept)', model)

    for old_module in MERGED_MODULES:
        # 1a. rename-on-collision, matching the renames done in the moved XML
        cr.execute(
            """
            UPDATE ir_model_data d
               SET module = 'l10n_pt_ao',
                   name = d.name || '_' || d.module
             WHERE d.module = %s
               AND EXISTS (SELECT 1 FROM ir_model_data d2
                            WHERE d2.module = 'l10n_pt_ao'
                              AND d2.name = d.name)
            """,
            (old_module,),
        )
        renamed = cr.rowcount
        # 1b. plain re-parent for everything else
        cr.execute(
            """
            UPDATE ir_model_data d
               SET module = 'l10n_pt_ao'
             WHERE d.module = %s
               AND NOT EXISTS (SELECT 1 FROM ir_model_data d2
                                WHERE d2.module = 'l10n_pt_ao'
                                  AND d2.name = d.name)
            """,
            (old_module,),
        )
        moved = cr.rowcount
        # 1c. anything still left is an exact duplicate of a core record —
        # drop only the metadata entry, never the referenced record
        cr.execute("DELETE FROM ir_model_data WHERE module = %s", (old_module,))
        dropped = cr.rowcount

        # 2. mark the old module as gone without triggering an uninstall
        cr.execute(
            """
            UPDATE ir_module_module
               SET state = 'uninstalled', latest_version = NULL
             WHERE name = %s
               AND state NOT IN ('uninstalled', 'uninstallable')
            """,
            (old_module,),
        )

        # 3. stale dependency rows of modules that used to depend on it
        cr.execute("DELETE FROM ir_module_module_dependency WHERE name = %s", (old_module,))

        _logger.info(
            'l10n_pt_ao merge: %s -> moved %s xml_ids (%s renamed, %s duplicates dropped)',
            old_module, moved, renamed, dropped,
        )
