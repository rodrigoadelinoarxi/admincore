# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    if not version:
        return

    env = api.Environment(cr, SUPERUSER_ID, {})

    env['hr.salary.rule'].search([
        ('code', 'in', ['IRSVM', 'IRSVACSUB', 'IRSCHRSUB', 'IRSMEALSUB']),
    ]).write({
        'employee_total_income': True,
        'employee_irs_deducted': True,
    })

    env['hr.salary.rule'].search([
        ('code', 'in', ['SS', 'SSVAC', 'SSCHR']),
    ]).write({
        'employee_ss_deducted': True,
    })

    env['hr.employee'].with_context(active_test=False).search([])._get_annual_report_values()
