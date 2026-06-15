from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site_constructor', '0015_fixed'),
    ]

    operations = [
        migrations.RunSQL(
            sql="SELECT 1",  # ничего не делаем - таблица уже переименована
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]