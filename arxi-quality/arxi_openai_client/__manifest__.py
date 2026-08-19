{
    'name': 'Arxi OpenAI Client',
    'version': '19.0.1.0.0',
    'category': 'Technical',
    'summary': 'OpenAI API client wrapper for Odoo modules',
    'author': 'Arxi',
    'website': 'https://www.arxi.pt',
    'depends': ['base'],
    'data': [
        'data/ir_config_parameter.xml',
    ],
    # REVERTIDO 2026-08-19 11:52 UTC: o commit 0c63f44 (11:43) assumiu, so pelo
    # texto do manifesto de 6e30f65, que este modulo tinha sido recompilado
    # como os outros 31 do mesmo cluster PyArmor — mas 6e30f65 NAO tocou no
    # ficheiro pyarmor_runtime.so deste modulo (git log confirma so
    # '59c8aca Primeiro upload' no historico do .so). Confirmado por teste
    # direto (docker run odoo:19 + nm -D): o binario continua o mesmo de
    # 2026-07-29 (mtime, 792360 bytes) e continua a exportar
    # 'undefined symbol: _PyFloat_Pack8' — crash real reproduzido na run
    # 17_to_19_20260819_114418 (Couldn't load module arxi_openai_client).
    # Ao contrario dos outros 31 modulos do cluster (recompilados 2026-08-14,
    # sem essa simbolo em falta — confirmado por nm -D em todos), este
    # continua genuinamente por recompilar pela Arxi. Ver
    # memory/project_migracao_admincore_17_19.md.
    'installable': False,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
