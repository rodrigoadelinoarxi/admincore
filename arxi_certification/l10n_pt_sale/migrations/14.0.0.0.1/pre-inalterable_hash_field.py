def migrate(cr, version):
    cr.execute("""ALTER TABLE sale_order ADD COLUMN IF NOT EXISTS inalterable_hash VARCHAR""")
    cr.execute("""UPDATE sale_order SET inalterable_hash = hash""")
