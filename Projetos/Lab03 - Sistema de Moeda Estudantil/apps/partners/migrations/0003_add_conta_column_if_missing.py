# apps/partners/migrations/0003_add_conta_column_if_missing.py
from django.db import migrations, connection


def ensure_conta_column(apps, schema_editor):
    """
    Garante que a coluna 'conta_id' exista na tabela partners_empresaparceira.
    Em SQLite, criamos a coluna via SQL simples (sem constraint de FK).
    É idempotente: só cria se não existir.
    """
    table = "partners_empresaparceira"

    # Verifica colunas atuais
    with connection.cursor() as cursor:
        cols = [c.name for c in connection.introspection.get_table_description(cursor, table)]

    if "conta_id" in cols:
        return  # já existe, nada a fazer

    # Cria a coluna como INTEGER NULL
    schema_editor.execute(f'ALTER TABLE "{table}" ADD COLUMN "conta_id" integer NULL;')

    # (Opcional) criar índice simples para filtragens/joins
    schema_editor.execute(f'CREATE INDEX IF NOT EXISTS "{table}_conta_id_idx" ON "{table}" ("conta_id");')


class Migration(migrations.Migration):
    # Dependa apenas do estado inicial do app, para evitar conflitos
    dependencies = [
        ("partners", "0001_initial"),
        # não precisamos depender de accounts aqui, pois não vamos declarar FK nesta migração
    ]

    operations = [
        migrations.RunPython(ensure_conta_column, migrations.RunPython.noop),
    ]
