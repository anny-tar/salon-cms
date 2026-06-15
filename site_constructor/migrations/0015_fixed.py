from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_constructor', '0014_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='map_url',
            field=models.TextField(blank=True, help_text='Значение атрибута src из iframe Яндекс Карт', verbose_name='Ссылка карты'),
        ),
        migrations.AlterField(
            model_name='address',
            name='name',
            field=models.CharField(help_text='Например: «Главный офис», «Филиал на Ленина»', max_length=255, verbose_name='Название'),
        ),
    ]