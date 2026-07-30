{
    "name": "Restricted administration rights",
    "summary": "Apply strict restriction on what an admin can do",
    "version": "17.0.1.3.6",
    "author": "IT-Projects LLC, Ivan Yelizariev",
    "category": "Extra Tools",
    "images": ["images/banner.jpg"],
    "support": "apps@itpp.dev",
    "website": "https://twitter.com/OdooFree",
    "license": "Other OSI approved licence",  # MIT
    "currency": "EUR",
    "depends": ["ir_rule_protected"],
    "data": [
        "security/access_restricted_security.xml",
        "views/res_groups_views.xml"
    ],

    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    "installable": False,
}
