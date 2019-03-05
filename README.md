# Dathena File Server

This application supports the uploading of files and its respective metadata labels.

## Getting Started

You only need docker compose which will initialise the application.
```
docker-compose up
```
## APIs
There are two main categories of APIs in this application. One category is for file upload, and the other is for the general data labels.

### General Data Labels API

Categories for the <label\> : "lang", "doctype", "conf-level".

The value of the id <pk\> can only be retrieved by retrieving all labels first. e.g. [{ id: 1, name: English, short_name: en }, ...], where <pk\> is 1

#### CRUD for Labels

1) Retrieve all labels from the category
```
[GET] localhost:8000/<label>/
```
2) Create new label in one of the categories - creates a counter for the new label in a separate table as well
```
[POST] localhost:8000/<label>/
```
Parameters required in body form-data:
```
lang - (1) name: e.g. English, (2) short_name: e.g. en
doctype - (1) name: e.g. PDF
conf-level - (1) name: e.g. Secret
```
3) Retrieve one label from the category
```
[GET] localhost:8000/<label>/<pk>/
```
4) Update one label from the category
```
[PUT] localhost:8000/<label>/<pk>/
```
Parameters required in body form-data:
```
lang - (1) name: e.g. English, (2) short_name: e.g. en
doctype - (1) name: e.g. PDF
conf-level - (1) name: e.g. Secret
```
5) Delete one label from the category - deletes the counter for the label which is in another table
```
[DELETE] localhost:8000/<label>/<pk>/
```

#### Read and Update only for Label Counters - Creation and Deletion will be cascaded from Label CRUD

6) Retrieve all counters for all the labels in the specified category
```
[GET] localhost:8000/<label>/count/
```
7) Update one label counter from the category
```
[PUT] localhost:8000/<label>/count/<pk>
```
Parameters required in body form-data:
```
(1) total_docs: e.g. 10
```
### File Upload API
1) Retrieve a list of all files
```
[GET] localhost:8000/upload/
```
2) Create new file with metadata
```
[POST] localhost:8000/upload/
```
Parameters required in body form-data:
```
(1) language: <language pk> e.g. 1
(2) doctype: <doctype pk> e.g 1
(3) conf_level: <conflevel pk> e.g. 1
(4) file: <uploaded file> e.g. test.pdf
```
3) Update a file
```
[PUT] localhost:8000/upload/<pk>/
```
Parameters required in body form-data:
```
[OPTIONAL] (1) language: <language pk> e.g. 1
[OPTIONAL] (2) doctype: <doctype pk> e.g 1
[OPTIONAL] (3) conf_level: <conflevel pk> e.g. 1
[OPTIONAL] (4) file: <uploaded file> e.g. test.pdf
```
4) Retrieve a single file by id
```
[GET] localhost:8000/upload/<pk>/
```
5) Delete a file by id
```
[DELETE] localhost:8000/upload/<pk>/
```

## Cron Jobs (Periodic Tasks)
1) increment_docs - increments any two random labels from a random category every 5 seconds

2) count_files - counts total number of files every 10 seconds

## Implementation of Celery and Redis Message Queue

Celery was used to replace the processes of creation, update, and deletion of the General Data Labels API. Retrieval was left out as we need an instant response for reading. In further implementations, retrieval can be included by including a results backend for celery, which will be coupled with periodic pollings from the client side.

Celery was used to replace only the process of deletion of files due to the fact that we should not put complex data into the message queue (Redis). The location of the queue is in the memory which makes it unsuitable for large and complex data (e.g. file bytes).

Under normal circumstances, files should not be held in the application server, and should instead be stored in an external server like S3. In this circumstance, the files can be temporarily saved to the application server, and be queued to be uploaded to the external server.

Alternatively, if we really want to enqueue the file data into the message queue, we can first encode the file into a format suitable for celery's serializer (Kombu), and decode when the processing starts. However, this is highly unadvisable.

## Issues
Occasionally, upon docker-compose up, the error "ERROR: Pidfile (celerybeat.pid) already exists" may arise. To resolve this issue, simply delete the "celerybeat.pid" file in the root directory of the project.
