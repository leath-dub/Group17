# -*- encoding: utf-8 -*-


from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.shortcuts import get_object_or_404

from core.utils import mk_paginator
from .models import Cluster, Pod, Event


@login_required(login_url="/login/")
def index(request):
    context = {
        "segment": "index",
        "clusters": Cluster.objects.all(),
        "pods": Pod.objects.all(),
    }

    html_template = loader.get_template("home/index.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def get_pod_events(request, pod_id):
    pod = get_object_or_404(Pod, id=pod_id)
    events = Event.objects.filter(pod=pod)

    context = {
        "pod": pod,
        "events": mk_paginator(request, events, 5),
        "event_count": events.count(),
    }

    html_template = loader.get_template("includes/events.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def get_pod_status(request, pod_id):
    pod = get_object_or_404(Pod, id=pod_id)

    if pod.status == pod.DEAD:
        color = "red"
    elif pod.status == pod.ALIVE:
        color = "green"
    else:
        pod.status = "yellow"

    return JsonResponse({"color": color})


@login_required(login_url="/login/")
def get_pods(request):
    pods = Pod.objects.all()
    pod_data = [
        {
            "id": pod.id,
            "name": pod.name,
            "status": pod.status,
            "namespace": pod.namespace,
        }
        for pod in pods
    ]
    return JsonResponse({"pods": pod_data})


@login_required(login_url="/login/")
def pages(request):
    context = {}

    try:
        load_template = request.path.split("/")[-1]

        if load_template == "admin":
            return HttpResponseRedirect(reverse("admin:index"))
        context["segment"] = load_template

        html_template = loader.get_template("home/" + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        html_template = loader.get_template("home/page-404.html")
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template("home/page-500.html")
        return HttpResponse(html_template.render(context, request))
