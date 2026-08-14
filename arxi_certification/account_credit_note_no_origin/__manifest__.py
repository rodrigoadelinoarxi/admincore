# -*- coding: utf-8 -*-
{
    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': False,

    'name'       : "Credit Note No Origin",

    'summary'    : """
       A module to handle credit notes without origin in Odoo.""",
    'description': """
This module allows the creation of credit notes without an origin in Odoo. It is particularly useful for cases where a credit note needs to be issued without a corresponding invoice or sale order, providing flexibility in financial transactions.
   """,

    'author'     : "ARXILEAD",
    'website'    : "https://www.arxi.pt",

    'category'   : 'Uncategorized',
    'version'    : '19.0.0.0.1',
    'license': 'OPL-1',

    # any module necessary for this one to work correctly
    'depends'    : ['account', 'l10n_pt_ao'],
    'data'       : [
        'security/ir.model.access.csv',

        'wizards/missing_refund_origin_wizard_view.xml',
    ],
}
