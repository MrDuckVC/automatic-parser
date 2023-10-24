# Generated by Django 3.2.6 on 2022-04-13 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Launches',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_of_start', models.DateTimeField(auto_now_add=True, help_text='Дата начало парсинга', null=True)),
                ('type_of_parse', models.CharField(choices=[('deep', 'deep'), ('surface', 'surface'), ['total', 'total'], ['check', 'check']], help_text='Тип парсинга', max_length=128)),
                ('status', models.CharField(choices=[('In progress', 'In progress'), ('Done', 'Done'), ('Canceled', 'Canceled'), ('Failed', 'Failed')], help_text='Текущий статус', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='ScriptName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('script_name', models.CharField(help_text='Имя скрипта', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wine_json', models.JSONField()),
                ('hash', models.CharField(max_length=40, unique=True)),
                ('launch_id', models.ManyToManyField(help_text='Id запусков', to='main.Launches')),
            ],
        ),
        migrations.AddField(
            model_name='launches',
            name='script_name',
            field=models.ForeignKey(help_text='Имя скрипта', on_delete=django.db.models.deletion.DO_NOTHING, to='main.scriptname'),
        ),
        migrations.AddIndex(
            model_name='result',
            index=models.Index(fields=['hash'], name='main_result_hash_c2e898_idx'),
        ),
    ]