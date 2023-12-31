# Generated by Django 3.2.6 on 2022-05-12 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParsingJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_of_start', models.DateTimeField(auto_now_add=True, help_text='Date time of parsing start', null=True)),
                ('type_of_parse', models.CharField(choices=[('deep', 'deep'), ('surface', 'surface'), ['total', 'total'], ['check', 'check']], help_text='Parsing type', max_length=128)),
                ('status', models.CharField(choices=[('In progress', 'In progress'), ('Done', 'Done'), ('Canceled', 'Canceled'), ('Failed', 'Failed')], help_text='Current job status', max_length=128)),
            ],
        ),
        migrations.RemoveField(
            model_name='result',
            name='launch_id',
        ),
        migrations.AlterField(
            model_name='scriptname',
            name='script_name',
            field=models.CharField(help_text='Parser script name', max_length=128),
        ),
        migrations.DeleteModel(
            name='Launches',
        ),
        migrations.AddField(
            model_name='parsingjob',
            name='script_name',
            field=models.ForeignKey(help_text='Script name', on_delete=django.db.models.deletion.DO_NOTHING, to='main.scriptname'),
        ),
        migrations.AddField(
            model_name='result',
            name='parsing_job_id',
            field=models.ManyToManyField(help_text='Parser run Id', to='main.ParsingJob'),
        ),
    ]
