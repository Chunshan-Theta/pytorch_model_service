import json
import datetime

from senti import senti
from util.aredis_queue import NLUQueue
import asyncio
import os
task_name = 'common' if 'task_name' not in os.environ else os.environ['task_name']
redis_to_MDL = NLUQueue(name="MDL", namespace=task_name, host='127.0.0.1', port=6379)
redis_to_API = NLUQueue(name="API", namespace="common", host='127.0.0.1', port=6379)


async def get_work():
    res = await redis_to_MDL.dequeue_nowait()
    print(f"get_work: {res}")
    res = json.loads(res) if res is not None else None
    return res


async def send_responds(obj, request_id):
    obj["worker"] = task_name
    print(f"send_responds: {obj}")
    return_value = json.dumps(obj, ensure_ascii=False)
    return await redis_to_API.set_msg_by_direct_id_ex(id=request_id, second2expire=300, value=return_value)


async def send_heartbeats():
    return await redis_to_API.enqueue({"status": True, "label": f"sample worker, task_name:{task_name}", "datetime":str(datetime.datetime.now())})


async def main():
    idx = 0
    while True:
        task = await get_work()
        if task is not None:
            obj = task.get("obj", None)
            request_id = task.get("request_id", None)
            sentence = obj.get("sentence", "A單位與案家討論完服務後會有同意書的範本嗎")
            result = senti(sentence)


            #
            await send_responds({
                "ans": result
            }, request_id)
        else:
            idx += 1
            if idx == 30:
                #await send_heartbeats()
                idx = 0
            await asyncio.sleep(1)


asyncio.run(main())