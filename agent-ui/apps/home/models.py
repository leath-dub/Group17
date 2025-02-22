# -*- encoding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User


class Cluster(models.Model):
    pass


class Pod(models.Model):
    ALIVE = 'Alive'
    AFFECTED = 'Affected'
    DEAD = 'Dead'

    POD_STATUS = [
        (ALIVE, ALIVE),
        (AFFECTED, AFFECTED),
        (DEAD, DEAD),
    ]

    cluster = models.ForeignKey(
        Cluster,
        on_delete=models.CASCADE
    )
    namespace = models.CharField(
        max_length=255,
    )
    status = models.CharField(
        choices=POD_STATUS, max_length=10, default=ALIVE)
