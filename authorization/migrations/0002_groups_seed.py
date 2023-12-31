# Generated by Django 2.2.1 on 2020-07-04 10:37

from django.core.management import call_command
from django.db import migrations


def load_fixture(apps, schema_editor):
    call_command("loaddata", "seed_groups", app_label="authorization")


class Migration(migrations.Migration):
    dependencies = [
        ("authorization", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]
