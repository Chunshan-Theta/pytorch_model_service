# Quick to start
```
docker-compose build
docker-compuse up
```

# Structure
![image](http://20.48.113.118/ai_team/ai_server/raw/8e52233cc43d0942a533afd544c249bff7cf4b29/doc/%E8%AA%9E%E6%84%8F%E6%A0%B8%E5%BF%83.001.jpeg)

```
 ｜
 ｜- master_server	
 ｜- model_worker
 ｜- redis_server	
 ｜- docker-compose.yml
```
- master_server: Master Server: main process for Restful API Requests
- redis_server: Jobs pool: stored jobs, job results and worker status reports
- model_worker: Worker(Mock): require jobs from Jobs pool and just throw mock result.

# Demo Line
