# Generated by Django 5.2.1 on 2025-05-18 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tarefas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarefa',
            name='finalizar',
            field=models.BooleanField(default=False),
        ),
    ]
