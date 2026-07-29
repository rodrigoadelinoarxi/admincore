# Copyright 2015-2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = ["multi.company.abstract", "product.template"]
    _name = "product.template"

    # No override needed - parent handles everything


class ProductProduct(models.Model):
    _inherit = ["multi.company.abstract", "product.product"]
    _name = "product.product"

    # Variant inherits company_ids from template (not its own M2M)
    company_ids = fields.Many2many(
        related="product_tmpl_id.company_ids",
        string="Companies",
        readonly=False,
    )

    # Remove company_id from prefetch to force recalculation
    # This ensures company_id always reflects current context
    def _read(self, fields):
        """Override to exclude company_id from prefetch."""
        # Never prefetch company_id - it must be computed fresh each time
        if fields and 'company_id' in fields:
            fields = [f for f in fields if f != 'company_id']
        return super()._read(fields)

    @api.depends("product_tmpl_id.company_ids")
    @api.depends_context("company", "_check_company_source_id")
    def _compute_company_id(self):
        """Override to use multi.company.abstract logic, but read company_ids from template."""
        for variant in self:
            # Get company_ids from template
            company_ids = variant.product_tmpl_id.company_ids
            # Apply multi-company logic
            company_id = (
                self.env.context.get("_check_company_source_id")
                or self.env.context.get("force_company")
                or self.env.company.id
            )
            if company_id in company_ids.ids:
                variant.company_id = company_id
            else:
                variant.company_id = company_ids[:1].id

    def _setup_complete(self):
        """Force override company_id field after all inheritance is processed."""
        super()._setup_complete()

        # Force replace the related field with computed field
        # This is needed because Odoo base has company_id = related('product_tmpl_id.company_id')
        # and we need it to be a computed field that respects context
        if "company_id" in self._fields:
            field = self._fields["company_id"]
            field.store = False
            field.related = None
            field.compute = "_compute_company_id"
            field.inverse = "_inverse_company_id"
            field.search = "_search_company_id"
            field.depends = ("product_tmpl_id.company_ids",)
            field.depends_context = ("company", "_check_company_source_id")