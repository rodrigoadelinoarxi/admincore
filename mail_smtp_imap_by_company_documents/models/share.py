from odoo import models, api


class DocumentShare(models.Model):
    _inherit = 'documents.share'

    def force_alias_domain(self, vals):
        if self.env.context.get('default_folder_id'):
            folder = self.env['documents.folder'].browse(self.env.context.get('default_folder_id'))
            if folder.company_id:
                alias_domain = self.env['alias.mail'].search([('company_id', '=', folder.company_id.id)], limit=1)
                if alias_domain:
                    vals['alias_domain'] = alias_domain.id
        return vals

    @api.model
    def create(self, vals):
        vals = self.force_alias_domain(vals)
        return super(DocumentShare, self).create(vals)

    def write(self, vals):
        vals = self.force_alias_domain(vals)
        return super(DocumentShare, self).write(vals)
