{
    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': False,

    'name'        : 'Portugal - Account Batch Payment',
    'summary'     : """
        Account Batch Payment
        """,

    'author'      : "ARXILEAD",
    'website'     : "https://www.arxi.pt",

    'category'    : 'Accounting & Finance',
    'version'     : '1.0',
    # Etapa 4.4 (2026-07-10): o modelo alvo (account.batch.payment.rejection)
    # foi removido na v19; a imutabilidade dos pagamentos certificados passou a
    # ser garantida pelos guards do core (l10n_pt_ao/l10n_pt_certificate).
    # Decisão: remover na v19 — mantido no repo apenas para histórico.
    'installable' : False,
    'license'     : 'OPL-1',

    'depends'     : ['account_batch_payment', 'l10n_pt_certificate'],
    'auto_install': True

}
