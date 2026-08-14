# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# Copyright 2016 Jacques-Etienne Baudoux <je@bcim.be>
# Copyright 2016 Sylvain Van Hoof <sylvain@okia.be>
# Copyright 2015-2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Detect changes and update the Account Chart from a template",
    "summary": "Wizard to update a company's account chart from a template",
    "version": "19.0.1.0.2",
    "author": "Tecnativa, BCIM, Okia, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/account-financial-tools",
    "depends": ["account", "l10n_generic_coa"],
    "category": "Accounting",
    "license": "AGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "wizard/wizard_chart_update_view.xml",
        "views/account_config_settings_view.xml",
    ],

    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    "installable": False,
}
