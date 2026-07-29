def fix_lines(self, path):
    import csv

    velcro_company_id = self.env['res.company'].browse(4)
    dict_builder = []

    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        next(reader)  # header
        for row in reader:
            dict_builder.append({
                'partner_name'  : row[0],
                'group_name'    : row[1],
                'project_name'  : row[2],
            })

    # Criar Grupos Analíticos
    for build in dict_builder:
        if group_name := build.get('group_name'):
            if analytic_group_id := self.env['account.analytic.group'].search([('company_id', '=', velcro_company_id.id), ('name', '=', group_name)]):
                build['account_analytic_group_id'] = analytic_group_id.id
            else:
                analytic_group_id = self.env['account.analytic.group'].create({
                    'name'      : group_name,
                    'company_id': velcro_company_id.id,
                })
                build['account_analytic_group_id'] = analytic_group_id.id

    # Criar Projetos
    for build in dict_builder:
        if project_name := build.get('project_name'):
            project_id = self.env['project.project'].create({
                'name'              : project_name,
                'company_id'        : velcro_company_id.id,
                'analytic_group_id' : build.get('account_analytic_group_id'),
                'allow_forecast'    : True,
                'allow_timesheets'  : True,
                'allow_billable'    : True,
            })
            if partner_name := build.get('partner_name'):
                if partner_id := self.env['res.partner'].search([('name', 'ilike', partner_name), '|', ('company_id', '=', velcro_company_id.id), ('company_id', '=', False)], limit=1):
                    project_id.analytic_account_id.write({
                        'partner_id': partner_id.id
                    })
