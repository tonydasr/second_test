# Generated by Django 4.2.1 on 2023-05-18 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_accountdetails_bitcoin_accountdetails_ethereum_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Userpassword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='contact_no',
            field=models.CharField(blank=True, default='+', max_length=30, null=True),
        ),
    ]