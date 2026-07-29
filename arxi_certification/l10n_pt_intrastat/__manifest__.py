{
    'name': "Portugal - Certified Intrastat",

    'summary': """
        Adds a button to export an csv with INE(WebINQ) format
    """,
    'author': "Arxi",
    'website': "https://www.arxi.pt",
    'category': 'Accounting & Finance',
    'version': '17.0.1.0.0',
    'license': 'OPL-1',
    'depends': ['l10n_pt_certificate', 'account_intrastat'],
    'data': [
        'reports/report_invoice.xml',
        'views/res_config_settings_views.xml'
    ],
    'auto_install': True,
}
