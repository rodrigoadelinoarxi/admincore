def import_custom_chart_of_templates(self, company):
    import csv
    with open(
            r'/home/administrator/PycharmProjects/server-casperventures/casperventures/Plano Contas Casper v2 2014.csv',
            newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader)  # header
        for row in reader:
            if not row[5] or not row[5].strip() or row[5] == 'account.data_unaffected_earnings':
                continue
            if row[5] == 'tko_account_pt_accounting.data_account_type_view':
                # find or create accunt group
                group = self.env['account.group'].search(
                    [('company_id', '=', company.id), ('code_prefix_start', '=', row[0])], limit=1
                )
                if not group:
                    group.create({
                        'name'             : row[1],
                        'code_prefix_start': row[0],
                        'code_prefix_end'  : row[0],
                        'company_id'       : company.id,
                    })
            else:
                # find or create account account
                account = self.env['account.account'].search(
                    [('company_id', '=', company.id), ('code', '=', row[0])], limit=1
                )
                if not account:
                    group = self.env['account.group'].search(
                        [('company_id', '=', company.id), ('code_prefix_start', '=', row[0])], limit=1
                    )
                if not account and not group:
                    user_type_id = self.env.ref(row[5])
                    account.create({
                        'name'        : row[1],
                        'code'        : row[0],
                        'user_type_id': user_type_id.id,
                        'reconcile'   : user_type_id.type in ('receivable', 'payable'),
                        'company_id'  : company.id
                    })
