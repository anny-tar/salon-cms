from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Синхронизирует состояние Django с реальной БД.
    Поле slug уже уникальное в БД (через RunSQL в 0002),
    но Django об этом не знает — исправляем через SeparateDatabaseAndState.
    """

    dependencies = [
        ('products', '0002_product_alt_text_product_h1_product_meta_description_and_more'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],  # В БД ничего не делаем — уже сделано
            state_operations=[
                migrations.AlterField(
                    model_name='product',
                    name='slug',
                    field=models.SlugField(
                        blank=True,
                        help_text='Заполняется автоматически. Можно изменить вручную.',
                        max_length=200,
                        unique=True,
                        verbose_name='URL (slug)',
                    ),
                ),
            ],
        ),
    ]
