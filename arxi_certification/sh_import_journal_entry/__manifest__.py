# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Import Multiple Journal Entries from CSV File | Import Multiple Journal Entries from Excel file",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Accounting",
    "summary": "Import Journal Entries From CSV Import Journal Entries From Excel Import Journal Entry From CSV import Journal Entry From Excel Import Mass Journal Import Multiple Journal import account move import opening journal import opening balance Odoo",
    "description": """This module is used to import multiple journal entries from CSV/Excel files. We provide the option to import analytic tags and all related to analytic accounts with journal entries. You can import multiple entries in a single click!""",
    "version": "17.0.0.1.2",
    "depends": [
        "sh_message",
        "account",
    ],
    "application": True,
    "data": [
        "security/import_journal_entry_security.xml",
        "security/ir.model.access.csv",
        "wizard/import_journal_entry_wizard.xml",
    ],
    'external_dependencies': {
        'python': ['xlrd'],
    },
    "images": ["static/description/background.png", ],
    "license": "OPL-1",
    "auto_install": False,

    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    "installable": False,
    "price": "15",
    "currency": "EUR"
}
