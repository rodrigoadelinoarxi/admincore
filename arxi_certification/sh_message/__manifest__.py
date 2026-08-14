# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Popup Message",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Extra Tools",
    "license": "OPL-1",
    "summary": "Create Success, warnings, alert message box wizard,success popup message app, alert popup module, email popup module odoo",
    "description": """This module is useful to create a custom popup message Wasting your important time to make popup message wizard-like Alert, Success, Warnings? We will help you to make this procedure quick, just add a few lines of code in your project to open the popup message wizard. """,
    "version": "19.0.0.0.2",
    "depends": ["base", "web"],
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "wizard/sh_message_wizard.xml",
    ],
    "images": ["static/description/background.jpg", ],
    "auto_install": False,

    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    "installable": False,
}
