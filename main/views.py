from celery.result import AsyncResult
from django.http import JsonResponse
from django.shortcuts import render
from time import sleep
from celery import shared_task, Celery
from django.core.cache import cache
from random import randint


app = Celery('cloud_test')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


def celery_status(request, task_id=None):
    try:
        # Inspect active workers
        inspector = app.control.inspect()
        active_workers = inspector.stats()

        worker_status = []
        if active_workers:
            for worker, stats in active_workers.items():
                worker_status.append({
                    "worker": worker,
                    "status": "Online",
                    "statistics": stats
                })
        else:
            worker_status.append({"status": "No active Celery workers found."})

        if task_id:
            task_result = AsyncResult(task_id)
            task_info = {
                "task_id": task_id,
                "task_status": task_result.status,
                "task_result": task_result.result
            }
        else:
            task_info = "No task ID provided. To check a specific task, include the task ID in the URL."

        response_data = {
            "worker_status": worker_status,
            "task_info": task_info,
        }

        return JsonResponse(response_data)

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@shared_task
def write_randoms(request):
    for n in range(10000):
        cache.set(n, randint(0, 100))

    return JsonResponse({"status": "success"})


def read_randoms(request):
    result = {}
    for n in range(10000):
        data = cache.get(n)
        if data:
            result[n] = data

    return JsonResponse(result if result else {"status": "empty"})


def clear_randoms(request):
    for n in range(10000):
        cache.delete(n)

    return JsonResponse({"status": "success"})
