# First Account Moves

def fix_lines(self, path):
    import csv

    line_builder = {}

    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        next(reader)  # header
        for row in reader:
            if row[0] in line_builder:
                cenas = line_builder.get(row[0]) + [row]
                line_builder[row[0]] = cenas
            else:
                line_builder[row[0]] = [row]

    # For each accounting move
    for key, vals in line_builder.items():

        # For each move line get the references
        move_reference = []
        move_dates = []
        move_accounts = []
        line_count = 0
        debit_val = 0
        for line_row in vals:
            move_reference.append(line_row[12])
            move_dates.append(line_row[9])
            move_accounts.append(line_row[1])
            if line_row[13]:
                debit_val += float(line_row[13].replace(',', ''))
            line_count += 1

        # Try to find the account move
        if move_id := self.env['account.move'].search([('ref', 'in', move_reference), ('date', 'in', move_dates)]):
            search_move_id = move_id.filtered(lambda m: len(m.line_ids) == line_count)
            if len(search_move_id) > 1:
                search_move_id = search_move_id.filtered(lambda m: m.amount_total == debit_val)
            if len(search_move_id) > 1:
                search_move_id = search_move_id.filtered(lambda m: all(code in move_accounts for code in m.line_ids.account_id.mapped('code')))
            for line_row in vals:
                if line_row[3]:
                    analytic_account_id = self.env['account.analytic.account'].browse(int(line_row[3]))
                    search_move_id.line_ids.filtered(lambda l: l.account_id.code == line_row[1]).write({
                        'analytic_account_id': analytic_account_id.id,
                    })
                if line_row[6]:
                    vehicle_id = self.env['fleet.vehicle'].search([('license_plate', '=', line_row[6].strip().replace(' ', ''))])
                    search_move_id.line_ids.filtered(lambda l: l.account_id.code == line_row[1]).write({
                        'vehicle_id': vehicle_id.id,
                    })
        else:
            print('Não encontrei nada!!! ', move_reference)


# fix_lines(self, '/home/luisfreitas/servers/server-casperventures/imp_novo.csv')
# fix_lines(self, '/tmp/imp_novo.csv')
# 22750, 22749, 22748, 22843, 22842, 23109, 23108, 23117, 23114, 23268, 23267, 23538, 23537

# September Account Moves
from odoo import fields


def fix_lines(self, path):
    import csv

    line_builder = {}

    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        next(reader)  # header
        for row in reader:
            if row[0] in line_builder:
                cenas = line_builder.get(row[0]) + [row]
                line_builder[row[0]] = cenas
            else:
                line_builder[row[0]] = [row]

    # For each accounting move
    for key, vals in line_builder.items():
        # For each move line get the references
        move_reference = []
        move_dates = []
        line_count = 0
        balance = 0
        for line_row in vals:
            move_reference.append(line_row[1])
            move_dates.append(fields.datetime.strptime(line_row[9], '%m/%d/%Y'))
            if line_row[6]:
                balance += float(line_row[6].replace(',', ''))
            line_count += 1

        # Try to find the account move
        if move_id := self.env['account.move'].search([('ref', 'in', move_reference), ('date', 'in', move_dates)]):
            search_move_id = move_id.filtered(lambda m: len(m.line_ids) == line_count)
            if len(search_move_id) > 1:
                search_move_id = search_move_id.filtered(lambda m: m.amount_total == balance)
            for line_row in vals:
                vals = {}
                move_line_id = search_move_id.line_ids.filtered(lambda l: l.account_id.code == line_row[2])
                if line_row[10]:
                    analytic_account_id = self.env['account.analytic.account'].browse(int(line_row[10]))
                    vals['analytic_account_id'] = analytic_account_id.id
                if line_row[12]:
                    license_plate = line_row[12].strip().replace(' ', '')
                    vehicle_id = self.env['fleet.vehicle'].search([('license_plate', '=', license_plate)])
                    vals['vehicle_id'] = vehicle_id.id
                if line_row[3] and not move_line_id.partner_id:
                    if partner_id := self.env['res.partner'].search([('name', 'ilike', line_row[3])]):
                        vals['partner_id'] = partner_id.id
                if vals:
                    move_line_id.write(vals)

                # Check if partner is in CSV and not in Odoo
                if line_row[3].replace(' ', '') and not move_line_id.partner_id:
                    print(f"Partner Not found! {line_row[0]} - {line_row[1]} - {line_row[3]}")
        else:
            print('Não encontrei nada!!! ', move_reference)
