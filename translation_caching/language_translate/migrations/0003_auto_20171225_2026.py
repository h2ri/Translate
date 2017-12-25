# Generated by Django 2.0 on 2017-12-25 14:56

from django.db import migrations, models


def load_stores(apps, schema_editor):
    l = apps.get_model("language_translate", "Language")
    a = l.objects.create(name="Dutch", label="nl")
    b = l.objects.create(name="English", label="en")
    c = l.objects.create(name="French", label="fr")
    d = l.objects.create(name="German", label="de")
    e = l.objects.create(name="Hebrew", label="iw")
    f = l.objects.create(name="Kannada", label="kn")
    a.related_name.add(c)
    c.related_name.add(d)
    c.related_name.add(e)
    d.related_name.add(c)
    d.related_name.add(b)



class Migration(migrations.Migration):

    dependencies = [
        ('language_translate', '0002_auto_20171220_2110'),
    ]

    operations = [
        migrations.RunPython(load_stores,)
    ]
