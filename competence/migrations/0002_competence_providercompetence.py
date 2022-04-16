# Generated by Django 4.0.4 on 2022-04-15 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('competence', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ProviderCompetence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competence.competence')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competence.provider')),
            ],
        ),
    ]
