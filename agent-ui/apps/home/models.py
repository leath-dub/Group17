# -*- encoding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User


class Cluster(models.Model):
    pass


class Pod(models.Model):
    ALIVE = "Alive"
    AFFECTED = "Affected"
    DEAD = "Dead"

    POD_STATUS = [
        (ALIVE, ALIVE),
        (AFFECTED, AFFECTED),
        (DEAD, DEAD),
    ]

    name = models.TextField(default="default")
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE)
    namespace = models.CharField(
        max_length=255,
    )
    status = models.CharField(choices=POD_STATUS, max_length=10, default=ALIVE)


class Event(models.Model):
    FAIL = "Failed"
    SUCCESS = "Success"
    PENDING = "Pending"

    EVENT_STATUS = [(FAIL, FAIL), (SUCCESS, SUCCESS), (PENDING, PENDING)]

    pod = models.ForeignKey(Pod, on_delete=models.CASCADE, null=True)
    status = models.CharField(choices=EVENT_STATUS, max_length=10, default=PENDING)
    name = models.CharField(max_length=255)
    event_id = models.IntegerField(unique=True, null=True)
    reply = models.TextField(null=True)
