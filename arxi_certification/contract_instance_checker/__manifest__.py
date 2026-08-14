# -*- coding: utf-8 -*-
{
    'name': 'Contract Instance Checker',
    'version': '19.0.1.0.2',
    'category': 'Services/Contract',
    'summary': 'Validação automática de contratos em instâncias controladas',
    'description': """
        Contract Instance Checker
        ==========================

        Módulo para instalação em instâncias controladas que valida automaticamente
        o contrato com o sistema central.

        Características:

        * Validação diária automática com sistema central via API
        * Alertas visuais quando contrato está próximo da expiração
        * Bloqueio automático da instância quando contrato expira
        * Controlo de limites de utilizadores
        * Alertas quando número de utilizadores excede o limite
        * Configuração simples via Settings (NIF, Token, URL central)
        * Sistema de segurança difícil de adulterar
    """,
    'author': 'FlyByOdoo',
    'website': 'https://www.flybyodoo.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'web',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/instance_checker_cron.xml',
        'views/res_config_settings_views.xml',
        'views/contract_status_templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'contract_instance_checker/static/src/scss/contract_alert.scss',
            'contract_instance_checker/static/src/scss/contract_banner.scss',
            'contract_instance_checker/static/src/js/contract_banner.js',
            'contract_instance_checker/static/src/xml/contract_banner.xml',
        ],
    },
    'demo': [],
    'images': ['static/description/icon.png'],

    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': False,
    'application': False,
    'auto_install': False,
}
