import asyncio

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from django.http import JsonResponse

# swagger
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from drf_yasg import openapi

#
from .util.aredis_queue import NLUQueue
import uuid
import json


def index(request):
    return HttpResponse("Hello, world. You're at the jobs_queue_service index.")




def hello_world(request):
    return render(request, 'hello_world.html', {
        'current_time': str(datetime.now()),
    })


async def worker_test(request):
    redis_to_API = NLUQueue(name="API", namespace="common")

    async def __new_work__(item: dict):
        task_name = "senti" if "task_name" not in item else item["task_name"][0]
        redis_to_MDL = NLUQueue(name="MDL", namespace=task_name)
        request_id = str(uuid.uuid4())
        task_str = json.dumps({
            "obj": item,
            "request_id": request_id
        },ensure_ascii=False)
        print(f"new_work: {task_str}")
        await redis_to_MDL.enqueue(task_str)
        return request_id

    async def __get_responds__(request_id: str):
        res = await redis_to_API.get_msg_by_direct_id(request_id)
        #print(f"{request_id} - get_responds: {res}")
        return res

    if str(request.method) == "GET":
        get_data = dict(request.GET)
        request_id = await __new_work__(get_data)
        worker_response = await __get_responds__(request_id)
        time = 0
        while worker_response is None and time < 500:
            worker_response = await __get_responds__(request_id)
            time += 1
            await asyncio.sleep(0.1)
        else:
            return JsonResponse({
                'get parameter': get_data,
                "worker response": json.loads(worker_response)
            }, json_dumps_params={"ensure_ascii": False})
    else:
        return HttpResponse("Only support GET method")


class MockRequest():
    def __init__(self, method, GET):
        self.method = method
        self.GET = GET

@swagger_auto_schema(
    method='POST',
    operation_summary='API',
    operation_description="""
    {
      "sentence":"A單位與案家討論完服務後會有同意書的範本嗎"
    }
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'sentence': openapi.Schema(type=openapi.TYPE_STRING)
        },
    )


)
@api_view(['POST'])
def worker_api(request: WSGIRequest):
    data = json.loads(request.body)
    # print(data["sentence"])
    # print(data["corpus"])

    #
    loop = asyncio.new_event_loop()
    dataset = MockRequest(GET=data, method="GET")
    result = loop.run_until_complete(worker_test(dataset))
    loop.close()
    return result
