from odoo import SUPERUSER_ID, api
import logging

_logger = logging.getLogger(__name__)

IDS = {'iva13_p_bc_ic': 'iva13_p_bi_ic', 'iva6_p_bc_ic' : 'iva6_p_bi_ic', 'iva13_p_s_ic' : 'iva13_p_s_ic_isp', 'iva6_p_s_ic' : 'iva6_p_s_ic_isp', 'iva23_p_bc_i' : 'iva23_p_bi_i', 'iva13_p_bc_i' : 'iva13_p_bi_i', 'iva6_p_bc_i' : 'iva6_p_bi_i', 'iva16_p_bc_i' : 'iva16_p_bi_i', 'iva9_p_bc_i' : 'iva9_p_bi_i',
           'iva4_p_bc_i' : 'iva4_p_bi_i', 'iva22_p_bc_i' : 'iva22_p_bi_i', 'iva12_p_bc_i' : 'iva12_p_bi_i', 'iva5_p_bc_i' : 'iva5_p_bi_i'}


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for id in IDS:
        for company in env['res.company'].search([]):
            tax = env.ref(f"account.{company.id}_{id}", raise_if_not_found=False)
            if tax:
                line = env['account.fiscal.position.tax'].search([('tax_dest_id', '=', tax.id)])
                line.tax_dest_id = env.ref(f"account.{company.id}_{IDS[id]}")




