# from odoo.addons.casperventures.scripts.copy_folders import copy_folders
# a = self.env['res.company'].browse(2)
# b = self.env['res.company'].browse(54)

def copy_folders(self, source_company, destination_company):
    folder_ids = self.env['documents.folder'].search([('company_id', '=', source_company)])
    for folder_id in folder_ids:
        company_id = destination_company
        created_folder_id = folder_id.copy()
        created_folder_id.company_id = company_id

        # Create tags for each folder
        # for facet_id in folder_id.facet_ids:
        #     vals_facet_id = facet_id.with_context(active_test=False).copy_data()[0]
        #     vals_facet_id['folder_id'] = created_folder_id.id
        #     created_facet_id = self.env['documents.facet'].with_context(lang=None).create(vals_facet_id)
        #     facet_id.with_context(from_copy_translation=True).copy_translations(created_facet_id,
        #                                                                         excluded=None or ())
        #
        #     # Create tags for each facet
        #     for tag_id in facet_id.tag_ids:
        #         vals_tag_id = tag_id.with_context(active_test=False).copy_data()[0]
        #         vals_tag_id['facet_id'] = created_facet_id.id
        #     try:
        #         created_tag_id = self.env['documents.tag'].with_context(lang=None).create(vals_tag_id)
        #         tag_id.with_context(from_copy_translation=True).copy_translations(created_tag_id,
        #                                                                           excluded=None or ())
        #     except Exception as e:
        #         print(e)


        # Create actions for each folder
        for action_id in self.env['documents.workflow.rule'].search([('domain_folder_id', '=', folder_id.id)]):
            created_action_id = action_id.copy()
            created_action_id.domain_folder_id = created_folder_id.id

            # Create Set tags action for each action
            for tag_action_id in action_id.tag_action_ids:
                tag_facet_id = self.env['documents.facet'].search(
                    [('folder_id', '=', created_folder_id.id), ('name', '=', tag_action_id.facet_id.name)],
                    limit=1)
                tag_id_id = self.env['documents.tag'].search(
                    [('facet_id', '=', tag_facet_id.id), ('name', '=', tag_action_id.tag_id.name)], limit=1)
                tag_action_vals = {
                    'workflow_rule_id': created_action_id.id,
                    'action'          : tag_action_id.action,
                    'facet_id'        : tag_facet_id.id,
                    'tag_id'          : tag_id_id.id,
                }
                self.env['documents.workflow.action'].create(tag_action_vals)

            if action_id.excluded_tag_ids:
                excluded_tag_ids = self.env['documents.tag'].search([
                    ('folder_id', '=', created_folder_id.id),
                    ('name', 'in', action_id.excluded_tag_ids.mapped('name'))
                ])
                created_action_id.write({'excluded_tag_ids': excluded_tag_ids.ids})

            if action_id.required_tag_ids:
                required_tag_ids = self.env['documents.tag'].search([
                    ('folder_id', '=', created_folder_id.id),
                    ('name', 'in', action_id.required_tag_ids.mapped('name'))
                ])
                created_action_id.write({'required_tag_ids': required_tag_ids.ids})

            if action_id.domain:
                created_action_id.domain = []

    # for folder_id in self.env['documents.folder'].search([]).filtered(lambda d: d.parent_folder_id):
    #     parent_folder_id = self.env['documents.folder'].search([
    #         ('name', '=', folder_id.parent_folder_id.name), ('company_id', '=', folder_id.company_id.id),
    #     ], limit=1)
    #     folder_id.parent_folder_id = parent_folder_id.id

# from odoo.addons.casperventures.scripts.copy_folders import adjust_created_folders
def adjust_created_folders(self):
    folder_ids = self.env['documents.folder'].search([('company_id', '=', 54)])
    for rec in folder_ids:
        print(rec.name)
        if rec.name not in ['Interno','Inbox','Financeiro','Tesouraria','Faturação','Contabilidade','Faturas de Fornecedor','RH','Marketing','Frota','Artigos','Recrutamento','Spreadsheet','Projectos']:
            rec.parent_folder_id = 120
