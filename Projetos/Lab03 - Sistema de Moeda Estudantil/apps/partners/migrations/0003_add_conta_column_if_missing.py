# apps/partners/migrations/0003_add_conta_column_if_missing.py
from django.db import migrations

def noop_forward(apps, schema_editor):
    """
    Esta migration existia originalmente para criar a coluna `conta_id`
    manualmente em SQLite, mas em bancos novos (ex.: Postgres no Render)
    ela causava conflito com a migration 0004, que já cria essa coluna.

    Agora ela é um NO-OP (não faz nada) para garantir que:

    - Em bancos antigos/local (SQLite): a migração já foi aplicada e isso
      não altera nada.
    - Em bancos novos (Render/Postgres): somente a migration 0004 cria
      `conta_id`, evitando o erro:
      
      `column "conta_id" already exists`
    """
    pass


def noop_reverse(apps, schema_editor):
    # não desfaz nada
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("partners", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(noop_forward, noop_reverse),
    ]
