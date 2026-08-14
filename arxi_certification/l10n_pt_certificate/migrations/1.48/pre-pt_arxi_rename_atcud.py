def _copy_column_if_exists(cr, table, old_column, new_column, column_type):
    """Add ``new_column`` (if missing) and copy over ``old_column``'s data
    (if it still exists) — safe to run on databases that already dropped
    the old column, or that never had it (fresh installs).
    """
    cr.execute(
        """ALTER TABLE %s ADD COLUMN IF NOT EXISTS %s %s"""
        % (table, new_column, column_type)
    )
    cr.execute(
        """
        SELECT EXISTS (
            SELECT FROM information_schema.columns
            WHERE table_schema = 'public'
            AND table_name = %s
            AND column_name = %s
        )
        """,
        (table, old_column),
    )
    if cr.fetchone()[0]:
        cr.execute(
            """UPDATE %s SET %s = %s WHERE %s IS NULL AND %s IS NOT NULL"""
            % (table, new_column, old_column, new_column, old_column)
        )


def migrate(cr, version):
    """Carry data over the ``pt_arxi_`` rename of ``atcud`` ->
    ``pt_arxi_atcud``, so older installations upgrading straight to this
    version don't lose the ATCUD already assigned to their certified
    documents/receipts.
    """
    for table in ("account_move", "account_payment"):
        _copy_column_if_exists(cr, table, "atcud", "pt_arxi_atcud", "VARCHAR")
