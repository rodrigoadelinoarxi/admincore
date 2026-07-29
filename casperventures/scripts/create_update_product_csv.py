def fix_lines(self, path):
    import csv
    from odoo import Command

    velcro_company_id = self.env['res.company'].browse(4)
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        next(reader)  # header
        for row in reader:
            # Can be sold / purchased
            vals = {
                'sale_ok'       : True if row[5] == 'VERDADEIRO' else False,
                'purchase_ok'   : True if row[6] == 'VERDADEIRO' else False,
                'company_ids'   : [Command.link(velcro_company_id.id)]
            }

            # Try to find product
            if product_id := self.env['product.template'].search([('default_code', '=', row[3])]):
                # Try to find client and supplier taxes
                if client_tax_id := self.env['account.tax'].search([('name', '=', row[9]), ('company_id', '=', velcro_company_id.id)]):
                    vals['taxes_id'] = [Command.link(client_tax_id.id)]
                if supplier_tax_id := self.env['account.tax'].search([('name', '=', row[10]), ('company_id', '=', velcro_company_id.id)]):
                    vals['supplier_taxes_id'] = [Command.link(supplier_tax_id.id)]
                # Try to find expenses and income accounts
                if row[16] and (expense_account_id := self.env['account.account'].search([('code', '=', row[16].strip().split(' ', 1)[0]), ('company_id', '=', velcro_company_id.id)])):
                    product_id.with_company(velcro_company_id).write({'property_account_expense_id': expense_account_id.id})
                if row[17] and (income_account_id := self.env['account.account'].search([('code', '=', row[17].strip().split(' ', 1)[0]), ('company_id', '=', velcro_company_id.id)])):
                    product_id.with_company(velcro_company_id).write({'property_account_income_id': income_account_id.id})
                product_id.write(vals)
            else:
                print(f'Not found {row[3]}')

# self.env['product.template'].search([])._compute_no_company_ids()

# def fix_lines(self, path):
#     import csv
#     from odoo import Command
#
#     company_id_78 = self.env['res.company'].browse(2)
#     with open(path, newline='') as csvfile:
#         reader = csv.reader(csvfile, delimiter=';', quotechar='"')
#         next(reader)  # header
#         for row in reader:
#             vals = {'company_ids'   : [Command.link(company_id_78.id)]}
#             # Try to find product
#             if product_id := self.env['product.template'].search([('default_code', '=', row[2])]):
#                 # Try to find client and supplier taxes
#                 if client_tax_id := self.env['account.tax'].search([('name', '=', row[8].strip()), ('company_id', '=', company_id_78.id)]):
#                     vals['taxes_id'] = [Command.link(client_tax_id.id)]
#                 if supplier_tax_id := self.env['account.tax'].search([('name', '=', row[9].strip()), ('company_id', '=', company_id_78.id)]):
#                     vals['supplier_taxes_id'] = [Command.link(supplier_tax_id.id)]
#                 # Try to find expenses and income accounts
#                 if row[15] and (expense_account_id := self.env['account.account'].search([('code', '=', row[15].strip().split(' ', 1)[0]), ('company_id', '=', company_id_78.id)])):
#                     product_id.with_company(company_id_78).write({'property_account_expense_id': expense_account_id.id})
#                 if row[16] and (income_account_id := self.env['account.account'].search([('code', '=', row[16].strip().split(' ', 1)[0]), ('company_id', '=', company_id_78.id)])):
#                     product_id.with_company(company_id_78).write({'property_account_income_id': income_account_id.id})
#                 product_id.write(vals)
#             else:
#                 print(f'Not found {row[3]}')

# self.env['product.template'].search([])._compute_no_company_ids()
