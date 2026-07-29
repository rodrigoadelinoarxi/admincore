from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for company in env['res.company'].search([('chart_template', '=', 'pt_arxi'), ('parent_id', '=', False)]):
        field_property_account_credit_note_customer_id = env['ir.model.fields']._get('product.template', 'property_account_credit_note_customer_id')
        field_property_account_credit_note_supplier_id = env['ir.model.fields']._get('product.template', 'property_account_credit_note_supplier_id')
        account_credit_note_customer_id = env.ref(f"account.{company.id}_chart_71711")
        account_credit_note_supplier_id = env.ref(f"account.{company.id}_chart_31711")
        env['ir.property'].create(
            {'name': 'property_account_credit_note_customer_id', 'fields_id': field_property_account_credit_note_customer_id.id, 'company_id': company.id, 'value_reference': f"account.account,{account_credit_note_customer_id.id}"})
        env['ir.property'].create(
            {'name': 'property_account_credit_note_supplier_id', 'fields_id': field_property_account_credit_note_supplier_id.id, 'company_id': company.id,
             'value_reference': f"account.account,{account_credit_note_supplier_id.id}"})