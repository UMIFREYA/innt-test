# Generated by Django 4.1.7 on 2023-03-22 07:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="IOS",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "ios_choices",
                    models.CharField(
                        choices=[
                            ("IOS X1", "IOS X1"),
                            ("IOS X2", "IOS X2"),
                            ("IOS X3", "IOS X3"),
                            ("IOS N", "IOS N"),
                        ],
                        default="IOS N",
                        max_length=10,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="NFT",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="XToken",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("total_supply", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Wallet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("PRIVATE", "Private Wallet"),
                            ("STUDIO", "Studio Wallet"),
                            ("AGENT", "Agent Wallet"),
                        ],
                        max_length=20,
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StudioTransaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.IntegerField()),
                (
                    "reason",
                    models.CharField(
                        choices=[
                            ("Fundraising", "Fundraising"),
                            ("Expense", "Expense"),
                            ("purchasing asset", "purchasing asset"),
                            ("Reason4", "Reason4"),
                        ],
                        max_length=20,
                    ),
                ),
                ("timestamp", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "receiver_wallet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="received_transactions",
                        to="ios.wallet",
                    ),
                ),
                (
                    "sender_wallet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sent_transactions",
                        to="ios.wallet",
                    ),
                ),
                (
                    "token",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="ios.xtoken"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Studio",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(max_length=255)),
                ("is_active", models.BooleanField(default=False)),
                (
                    "IOS_kernel",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("IOS X1", "IOS X1"),
                            ("IOS X2", "IOS X2"),
                            ("IOS X3", "IOS X3"),
                            ("IOS N", "IOS N"),
                        ],
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "agent_wallet",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="os_studios",
                        to="ios.wallet",
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "studio_wallet",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="os_studio",
                        to="ios.wallet",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="NFTBalance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "nft",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="ios.nft"
                    ),
                ),
                (
                    "wallet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="ios.wallet"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TokenBalance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("balance", models.IntegerField(default=0)),
                (
                    "wallet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="ios.wallet"
                    ),
                ),
                (
                    "x_token",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="ios.xtoken"
                    ),
                ),
            ],
            options={
                "unique_together": {("wallet", "x_token")},
            },
        ),
    ]
