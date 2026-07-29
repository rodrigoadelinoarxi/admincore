from odoo import SUPERUSER_ID, api
import logging

_logger = logging.getLogger(__name__)

TAX_IDS = ['iva23_p_bc_i', 'iva23_p_sp_ex', 'iva23_p_bi', 'iva23_p_nd', 'iva23_p_isp', 'iva13_p_s_ic', 'iva13_p_bc_ic', 'iva13_p_bc_i', 'iva13_p_sp_ex', 'iva13_p_bi', 'iva13_p_nd', 'iva13_p_isp',
           'iva6_p_s_ic', 'iva6_p_bc_ic', 'iva6_p_bc_i', 'iva6_p_bi', 'iva6_p_nd', 'iva6_p_isp', 'iva0_m03', 'iva0_m08', 'iva0_sp_i', 'iva0_sp_nd', 'iva0_p_bc', 'iva0_p_ns_b',
           'iva16isp', 'iva16_p_bc_i', 'iva16_p_sp_ex', 'iva16_p_bi', 'iva16_p_nd', 'iva9isp', 'iva9_p_bc_i', 'iva9_p_sp_ex', 'iva9_p_bi', 'iva9_p_nd', 'iva4isp', 'iva4_p_bc_i', 'iva4_p_sp_ex',
           'iva4_p_bi', 'iva4_p_nd', 'iva22isp', 'iva22_p_bc_i', 'iva22_p_sp_ex', 'iva22_p_bi', 'iva22_p_nd', 'iva12isp', 'iva12_p_bc_i', 'iva12_p_sp_ex', 'iva12_p_bi', 'iva12_p_nd',
           'iva5isp', 'iva5_p_bc_i', 'iva5_p_sp_ex', 'iva5_p_bi', 'iva5_p_nd']


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for company in env['res.company'].search([]):
        for id in TAX_IDS:
            if tax := env.ref(f"account.{company.id}_{id}", raise_if_not_found=False):
                tax.active = False

