def migrate(cr, version):
    cr.execute("""ALTER TABLE stock_picking ADD COLUMN IF NOT EXISTS inalterable_hash VARCHAR""")
    cr.execute("""UPDATE stock_picking SET inalterable_hash = hash""")
    cr.execute("""ALTER TABLE pt_transport ADD COLUMN IF NOT EXISTS inalterable_hash VARCHAR""")
    cr.execute("""UPDATE pt_transport SET inalterable_hash = hash""")
