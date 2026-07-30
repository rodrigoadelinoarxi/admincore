# Copyright 2018,2021 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2018 Ildar Nasyrov <https://it-projects.info/team/iledarn>
# License MIT (https://opensource.org/licenses/MIT).
{
    "name": """Control access to Apps""",
    "summary": """You can configure administrators which don't have access to Apps""",
    "category": "Extra Tools",
    # "live_test_url": "",
    "images": ["images/banner.png"],
    "version": "17.0.2.0.1",
    "application": False,
    "author": "IT-Projects LLC, Ivan Yelizariev",
    "support": "apps@itpp.dev",
    "website": "https://twitter.com/OdooFree",
    "license": "Other OSI approved licence",  # MIT
    # "price": 10.00,
    "currency": "EUR",
    "depends": ["access_restricted", "base_install_request"],
    "external_dependencies": {"python": [], "bin": []},
    "data": ["security/access_apps_security.xml", "security/ir.model.access.csv"],
    "demo": [],
    "qweb": [],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": "uninstall_hook",
    "auto_install": False,

    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    "installable": False,
}
