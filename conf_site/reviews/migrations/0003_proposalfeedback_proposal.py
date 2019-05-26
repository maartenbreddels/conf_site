# Generated by Django 2.0.13 on 2019-04-15 21:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0001_initial'),
        ('reviews', '0002_proposalfeedback_proposalresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalfeedback',
            name='proposal',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='review_feedback', to='proposals.Proposal'),
            preserve_default=False,
        ),
    ]