from django.db import migrations


class Migration(migrations.Migration):
    """
    Переименовывает таблицу site_constructor_saloncontact
    в site_constructor_contact в БД.
    """

    dependencies = [
        ('site_constructor', '0015_fixed'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql='ALTER TABLE site_constructor_saloncontact RENAME TO site_constructor_contact;',
                    reverse_sql='ALTER TABLE site_constructor_contact RENAME TO site_constructor_saloncontact;',
                ),
            ],
            state_operations=[
                migrations.RenameModel(
                    old_name='SalonContact',
                    new_name='Contact',
                ),
            ],
        ),
    ]
