# -*- encoding: utf-8 -*-

{
    'name'       : 'Portuguese Payroll',
    'category'   : 'Localization/Payroll',
    'author'     : 'ARXILEAD',
    'website'    : 'http://arxi.pt/',
    'depends'    : [
        'hr_payroll',
        'hr_work_entry',
        'hr_payroll_holidays',
        'hr_payroll_account',
        'hr_payroll_account_sepa'
    ],
    'version'    : '17.0.0.0.62',
    'license'    : 'OPL-1',
    'description': """

Portuguese Payroll Rules
========================

    - Configuration of hr_payroll for Portuguese localization
    - Updated with IRS data
    """,
    'data'       : [
        # DATA
        'data/ss_regime_data.xml',
        'data/leave_type_data.xml',
        'data/work_entry_type.xml',
        'data/structure.xml',
        'data/work_entry_type_structure_link.xml',
        'data/rule_category.xml',
        'data/rules.xml',
        'data/rules_deduction.xml',
        'data/input_rules.xml',
        'data/hr_contract_type.xml',
        'data/payslip_email_template.xml',
        'data/irs_tax_table.xml',

        'security/security.xml',
        'security/ir.model.access.csv',

        # VIEWS
        'wizard/export_dmr_views.xml',
        'wizard/export_dri_views.xml',
        'wizard/export_income_views.xml',
        'wizard/export_deductions_views.xml',
        'wizard/export_insurance_map_views.xml',
        'wizard/hr_payroll_payslips_by_employees_views.xml',
        'views/res_company.xml',
        'views/contract_view.xml',
        'views/employee_view.xml',
        'views/export_dmr_menu.xml',
        'views/hr_salary_rule.xml',
        # 'views/hr_salary_attachment_views.xml',
        'views/hr_payslip_view.xml',
        'views/hr_payslip_run_view.xml',
        'views/irs_tax_table_view.xml',
        'views/ss_regime_views.xml',
        'views/hr_work_entry_views.xml',

        # REPORTS
        'reports/payslip_report.xml',
        'reports/annual_income_report.xml',
        'reports/hr_payslips_export_income.xml',
    ],
}
