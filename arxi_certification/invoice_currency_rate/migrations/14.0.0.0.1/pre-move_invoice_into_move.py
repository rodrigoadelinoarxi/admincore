def migrate(cr, version):
    cr.execute("""ALTER TABLE account_move ADD COLUMN IF NOT EXISTS currency_rate NUMERIC""")
    cr.execute(
        """
        UPDATE account_move
        SET currency_rate = ai.currency_rate
        FROM account_invoice ai
        WHERE ai.move_id = account_move.id
        """
    )
