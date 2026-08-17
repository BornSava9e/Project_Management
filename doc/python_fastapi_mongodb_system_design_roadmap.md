# Python FastAPI + MongoDB + System Design Project Roadmap

## Project: Team Project & Issue Management System

A 2–3 week backend project designed to learn Python properly through a real FastAPI application.

The project covers:
- Python
- FastAPI
- Pydantic
- PyMongo
- MongoDB
- REST APIs
- JWT authentication
- Authorization
- Dependency Injection
- Middleware
- Error handling
- pytest
- Logging
- Rate limiting
- Redis
- Caching
- Background jobs
- Scheduler
- Queues
- Memory management
- Async programming
- Scaling
- Reliability
- System design

There is no frontend requirement. Use Postman and FastAPI Swagger/OpenAPI for testing.

---

# Main Learning Goal

The goal is not just to finish CRUD.

You should learn how to:
- Design a backend feature before coding.
- Decide what should be a function.
- Know when a class is useful.
- Understand FastAPI request handling.
- Understand Pydantic validation.
- Understand dependency injection.
- Build authentication and authorization.
- Work directly with MongoDB using PyMongo.
- Write tests.
- Understand production backend architecture.
- Explain scaling, caching, queues, rate limiting, scheduling, memory and reliability.

---

# Learning Rule

Do not force Python concepts into the project.

Use a concept when the problem naturally requires it.

```text
Repeated authentication logic -> dependency
Reusable database operation -> function/repository function
Different objects sharing behavior -> class/OOP
Large amount of data -> generator/cursor
Resource cleanup -> context manager
Cross-cutting request logic -> middleware
Centralized errors -> custom exceptions + handlers
Expensive/non-blocking work -> background worker
Repeated expensive reads -> cache
```

Your natural style is to create functions. That is completely fine.

Do not create classes just because you are learning OOP.

---

# Technology Stack

## Required

```text
Python
FastAPI
Uvicorn
PyMongo
MongoDB
Pydantic
pytest
python-dotenv
JWT library
password hashing library
Git
Postman
```

## Later / Advanced

```text
Redis
Background worker
Scheduler
Queue
Docker
Gunicorn
```

Only add a technology when the roadmap reaches it.

---

# High-Level Architecture

Start simple:

```text
Client
   |
   v
FastAPI
   |
   v
Business Logic
   |
   v
PyMongo
   |
   v
MongoDB
```

Later understand:

```text
Client
   |
   v
Load Balancer
   |
   +------------------+
   |                  |
   v                  v
FastAPI Instance 1  FastAPI Instance 2
   |                  |
   +--------+---------+
            |
      +-----+------+
      |            |
      v            v
    Redis       MongoDB
      |
      v
    Queue
      |
      v
   Workers
```

You do not need to implement every production component. You should understand why each exists.

---

# Suggested Final Project Structure

Start small and gradually reach:

```text
project-management-api/
|
├── app/
│   ├── config/
│   │   └── settings.py
│   ├── database/
│   │   └── connection.py
│   ├── routes/
│   ├── services/
│   ├── repositories/
│   ├── models/
│   ├── schemas/
│   ├── dependencies/
│   ├── middleware/
│   ├── exceptions/
│   └── utils/
|
├── tests/
├── .env
├── .gitignore
├── requirements.txt
└── run.py
```

Do not create every folder immediately.

---

# MongoDB

Use MongoDB directly through PyMongo.

Do not use MongoEngine or another ODM.

```text
FastAPI
   |
   v
PyMongo
   |
   v
MongoDB
```

Main collections:

```text
users
projects
tasks
comments
notifications
refresh_tokens
```

## Users

```text
_id
name
email
password_hash
role
created_at
updated_at
last_login_at
```

Roles:

```text
admin
manager
developer
```

## Projects

```text
_id
name
description
owner_id
members
status
created_at
updated_at
```

## Tasks

```text
_id
project_id
title
description
created_by
assigned_to
status
priority
due_date
tags
created_at
updated_at
completed_at
```

Status:

```text
todo
in_progress
completed
blocked
```

Priority:

```text
low
medium
high
critical
```

## Comments

```text
_id
task_id
user_id
message
created_at
updated_at
```

## Notifications

```text
_id
user_id
type
message
read
created_at
```

## Refresh Tokens

```text
_id
user_id
token_hash
expires_at
created_at
revoked
revoked_at
```

---

# FastAPI Concepts

Learn these throughout the project:

```text
FastAPI application
Path operations
GET / POST / PUT / PATCH / DELETE
Path parameters
Query parameters
Request body
Response models
Status codes
Pydantic
Dependency Injection
Depends
Routers
Middleware
Exception handlers
Background tasks
OpenAPI
Swagger UI
Async / await
```

---

# Authentication

Authentication answers:

> Who are you?

Authorization answers:

> Are you allowed to perform this action?

Keep them separate.

## Registration

```text
POST /auth/register
```

Input:

```text
name
email
password
```

Logic:

```text
Validate
-> validate email/password
-> check duplicate email
-> hash password
-> create user
-> store in MongoDB
-> return response
```

Never store plain-text passwords.

## Login

```text
POST /auth/login
```

Logic:

```text
Validate
-> find user
-> verify password
-> generic failure if invalid
-> generate access token
-> generate refresh token
-> store refresh-token state
-> update last login
-> return tokens
```

Do not reveal whether the email exists.

## Access Token

Use a short-lived JWT, for example 15–30 minutes.

Possible claims:

```text
user_id
role
issued_at
expiration
```

Do not store every access token in MongoDB.

## Refresh Token

Use a longer-lived refresh token.

Flow:

```text
Login
  |
  +--> Access Token
  |
  +--> Refresh Token
```

```text
Refresh Token
      |
      v
POST /auth/refresh
      |
      v
validate
      |
      v
check expiry/revocation
      |
      v
new access token
```

## Logout

```text
POST /auth/logout
```

Revoke the refresh-token state.

Understand that a stateless access token normally remains valid until expiration.

---

# FastAPI Dependency Injection

Learn FastAPI's dependency system.

Concept:

```text
Protected API
      |
      v
Authentication dependency
      |
      v
Verify JWT
      |
      v
Get current user
      |
      v
Route
```

Learn:

```text
Depends
dependency functions
reusable dependencies
dependency composition
```

This is one of the important FastAPI concepts for this project.

---

# Authorization

Roles:

```text
admin
manager
developer
```

Possible rules:

```text
Admin -> user/admin management
Project owner -> project/member management
Manager -> task management/assignment
Developer -> permitted project tasks/comments
```

Define the final permission matrix yourself.

Possible business functions:

```text
is_admin()
is_project_owner()
is_project_member()
can_manage_project()
can_modify_task()
can_assign_task()
```

---

# API Requirements

## Users

```text
GET    /users
GET    /users/<id>
PUT    /users/<id>
DELETE /users/<id>
```

## Projects

```text
POST   /projects
GET    /projects
GET    /projects/<id>
PUT    /projects/<id>
DELETE /projects/<id>
```

## Project Members

```text
GET    /projects/<id>/members
POST   /projects/<id>/members
DELETE /projects/<id>/members/<user_id>
```

## Tasks

```text
POST   /projects/<id>/tasks
GET    /projects/<id>/tasks
GET    /tasks/<id>
PUT    /tasks/<id>
DELETE /tasks/<id>
PATCH  /tasks/<id>/status
PATCH  /tasks/<id>/assign
```

## Comments

```text
POST   /tasks/<id>/comments
GET    /tasks/<id>/comments
DELETE /comments/<id>
```

## Notifications

```text
GET   /notifications
PATCH /notifications/<id>/read
```

## Statistics

```text
GET /projects/<id>/statistics
```

---

# Task Business Rules

When creating a task:

```text
Authenticate
-> validate
-> project exists
-> user is project member
-> validate assignee
-> create task
-> save
-> create notification
```

Status:

```text
todo
  |
  v
in_progress
  |
  +----> completed
  |
  +----> blocked
              |
              v
         in_progress
```

Define and enforce your own valid transitions.

---

# Search / Filtering / Sorting / Pagination

Search:

```text
GET /tasks?search=payment
```

Filter:

```text
?status=in_progress
?priority=high
?assigned_to=<id>
?project_id=<id>
```

Combination:

```text
?status=in_progress&priority=high
```

Sorting:

```text
?sort=created_at&order=desc
```

Pagination:

```text
?page=1&limit=20
```

Return:

```text
data
page
limit
total
total_pages
```

Whitelist sort fields and build MongoDB queries safely.

---

# MongoDB Aggregation

Statistics endpoint:

```text
GET /projects/<id>/statistics
```

Return:

```text
total_tasks
completed_tasks
in_progress_tasks
todo_tasks
blocked_tasks
high_priority_tasks
tasks_per_developer
```

Learn:

```text
$match
$group
$sort
$count
$lookup
```

---

# Validation with Pydantic

Learn:

```text
BaseModel
fields
types
optional fields
defaults
field validation
nested models
response models
```

Use Pydantic for API boundaries.

Business rules remain in business logic.

---

# Error Handling

Create meaningful application exceptions:

```text
UserNotFound
ProjectNotFound
TaskNotFound
Unauthorized
Forbidden
ValidationError
DuplicateResource
```

Learn FastAPI exception handlers and consistent error responses.

Common status codes:

```text
200
201
204
400
401
403
404
409
422
429
500
```

---

# Middleware

Use middleware for cross-cutting concerns such as:

```text
request ID
request logging
timing
security headers
```

Do not put business logic into middleware.

---

# Logging

Use Python logging.

Log:

```text
requests
login success/failure
important business operations
database errors
unexpected exceptions
```

Never log:

```text
passwords
JWTs
refresh tokens
sensitive information
```

---

# Testing

Use pytest.

Test:

```text
authentication
authorization
projects
tasks
comments
notifications
validation
errors
pagination
statistics
```

Test business rules, not only successful responses.

Examples:

```text
No token -> 401
Invalid token -> 401
No permission -> 403
Missing resource -> 404
Duplicate email -> 409
Invalid input -> 400/422
Too many requests -> 429
```

---

# Advanced System Design Track

## Rate Limiting

Learn:

```text
Fixed Window
Sliding Window
Token Bucket
Leaky Bucket
```

Start with login protection.

Later understand distributed rate limiting with Redis.

Questions:

```text
Why Redis?
Why not local memory?
What happens with multiple FastAPI instances?
What happens if one instance restarts?
```

---

# Redis

Use Redis later for:

```text
rate limiting
caching
distributed locks
temporary state
```

Understand what problem Redis solves in each case.

---

# Caching

Use an expensive endpoint such as project statistics.

Concept:

```text
Request
   |
   v
Redis
   |
   +--> hit -> response
   |
   +--> miss
           |
           v
        MongoDB
           |
           v
       store cache
           |
           v
        response
```

Learn:

```text
cache hit
cache miss
TTL
cache-aside
cache invalidation
cache stampede
```

---

# Scheduler

Add scheduled operations:

```text
Every hour:
    remove expired refresh tokens

Every day:
    find overdue tasks

Every night:
    generate report
```

Learn:

```text
Cron
APScheduler
Scheduler vs Worker
Celery Beat
```

Understand why heavy scheduled work should go through a queue/worker.

---

# Background Jobs and Queues

Concept:

```text
FastAPI
   |
   v
Queue
   |
   v
Worker
   |
   v
MongoDB / external API
```

Learn:

```text
producer
consumer
queue
worker
retry
dead-letter queue
```

---

# Idempotency

Understand duplicate requests:

```text
Client
  |
  v
Server processes
  |
  v
Network timeout
  |
  v
Client retries
```

Use an idempotency key concept for operations where duplicates are harmful:

```text
Idempotency-Key: unique-request-id
```

Learn why idempotency matters in distributed systems.

---

# Retry / Backoff

Learn:

```text
maximum retries
exponential backoff
jitter
retryable errors
non-retryable errors
dead-letter queue
```

Do not blindly retry every error.

---

# Timeouts

Use sensible timeouts for:

```text
MongoDB
HTTP APIs
external services
background jobs
```

Understand why no timeout can consume workers and overload the system.

---

# Circuit Breaker

Understand:

```text
CLOSED -> normal

OPEN -> stop calls temporarily

HALF-OPEN -> test recovery
```

You do not need a full production implementation.

---

# Memory Management

Learn:

```text
stack
heap
references
reference counting
garbage collection
object lifetime
mutable vs immutable
shallow copy
deep copy
generators
```

Exercise:

Compare loading one million MongoDB documents into a list versus processing through a MongoDB cursor/generator.

---

# Python Concurrency

Understand:

```text
process
thread
asyncio
async/await
GIL
CPU-bound
I/O-bound
```

Do not make everything async just because FastAPI supports it.

Understand when async helps.

---

# Scaling

Vertical:

```text
One server
  |
  +--> more CPU
  +--> more RAM
```

Horizontal:

```text
Server 1
Server 2
Server 3
```

Understand why stateless FastAPI services are easier to scale horizontally.

---

# Load Balancer

Production concept:

```text
Client
  |
  v
Load Balancer
  |
  +--> FastAPI 1
  +--> FastAPI 2
  +--> FastAPI 3
```

Learn:

```text
health checks
traffic distribution
instance failure
sticky sessions
stateless APIs
```

---

# Production Server

Understand:

```text
Load Balancer
      |
      v
Gunicorn/Uvicorn workers
      |
      +--> FastAPI worker
      +--> FastAPI worker
      +--> FastAPI worker
```

Learn workers, processes, timeouts, health checks and graceful shutdown.

---

# Database Connection Pooling

Understand why this is dangerous:

```text
10,000 requests
      |
      v
10,000 database connections
```

Learn:

```text
connection pooling
maximum pool size
timeouts
connection reuse
```

PyMongo manages reusable connections through its client/pool behavior.

---

# Distributed Locks

Scenario:

```text
Worker 1 ----+
             |
             v
        Same scheduled job
             ^
             |
Worker 2 ----+
```

Learn how distributed locks can prevent duplicate processing.

Redis is one possible implementation.

---

# Observability

Learn the difference:

```text
Logs
Metrics
Traces
```

Metrics:

```text
requests per second
error rate
latency
p95 latency
CPU
memory
database latency
cache hit rate
```

---

# Health Checks

Build:

```text
GET /health
```

Understand:

```text
liveness
readiness
```

Liveness:

> Is the application alive?

Readiness:

> Is it ready to receive traffic?

---

# Graceful Shutdown

Understand:

```text
shutdown signal
-> stop accepting new work
-> finish existing work
-> close resources
-> exit
```

---

# API Versioning

Understand:

```text
/api/v1/tasks
/api/v2/tasks
```

Why changing an API can `break existing clients.

---

# Security

Learn:

```text
CORS
CSRF
input validation
NoSQL injection
security headers
request size limits
rate limiting
secret management
```

---

# 14-Day Core Plan

## Day 1 — Setup

```text
[x] Create project directory
[x] Create Python virtual environment
[x] Install FastAPI
[x] Install Uvicorn
[x] Install PyMongo
[x] Install Pydantic
[x] Install pytest
[x] Install python-dotenv
[x] Install JWT/password hashing dependencies
[x] Create requirements file
[x] Create Git repository
[x] Create .gitignore
[x] Create .env
[x] Create FastAPI application
[x] Start server with Uvicorn
[x] Connect MongoDB
[x] Verify database connection
```

Learn before coding:

```text
Python venv
pip
requirements.txt
FastAPI basics
Uvicorn basics
FastAPI path operations
PyMongo connection
Pydantic basics
environment variables
Git basics
```

Do not learn authentication, Redis, async architecture or system design on Day 1.

## Day 2 — FastAPI Structure

```text
[X] Routers
[x] Configuration
[x] Database connection module
[x] Basic schemas
[x] Basic error handling
[x] Health endpoint
[x] API prefix
[x] Swagger/OpenAPI review
```

Learn:

```text
APIRouter
Pydantic models
Depends basics
FastAPI structure
response models
status codes
```

## Day 3 — Registration

```text
[x] Registration endpoint
[x] Pydantic request schema
[x] Email validation
[x] Password validation
[x] Duplicate email handling
[x] Password hashing
[x] User insertion
[x] Response schema
[x] Error handling
[x] Tests
```

## Day 4 — Login + JWT

```text
[ ] Login endpoint
[ ] Password verification
[ ] JWT access token
[ ] Token expiration
[ ] Authentication dependency
[ ] /auth/me
[ ] Invalid token handling
[ ] Expired token handling
[ ] Authentication tests
```

Learn:

```text
JWT
OAuth2 concepts
FastAPI security utilities
Depends
HTTP Bearer authentication
```

## Day 5 — Refresh Token + Logout

```text
[ ] Refresh token generation
[ ] Refresh token collection
[ ] Token hashing
[ ] Refresh endpoint
[ ] Expiration
[ ] Revocation
[ ] Logout
[ ] Tests
```

## Day 6 — Projects

```text
[ ] Project CRUD
[ ] Project owner
[ ] Project members
[ ] Permissions
[ ] Member APIs
[ ] Duplicate member protection
[ ] Owner protection
[ ] Tests
```

## Day 7 — Tasks

```text
[ ] Task CRUD
[ ] Task validation
[ ] Assignment
[ ] Status
[ ] Priority
[ ] Due date
[ ] Tags
[ ] Permission checks
[ ] Tests
```

## Day 8 — Search + Filtering + Pagination

```text
[ ] Search
[ ] Status filter
[ ] Priority filter
[ ] Assignee filter
[ ] Multiple filters
[ ] Sorting
[ ] Pagination
[ ] Validation
[ ] MongoDB indexes
```

## Day 9 — Comments + Notifications

```text
[ ] Comments
[ ] Comment permissions
[ ] Notifications
[ ] Task assignment notification
[ ] Completion notification
[ ] Comment notification
[ ] Mark notification read
```

## Day 10 — Aggregation

```text
[ ] Project statistics
[ ] Task counts
[ ] Status counts
[ ] Priority counts
[ ] Developer task counts
[ ] Aggregation pipeline
[ ] Tests
```

## Day 11 — Errors + Middleware + Logging

```text
[ ] Custom exceptions
[ ] FastAPI exception handlers
[ ] Consistent error responses
[ ] Middleware
[ ] Request ID
[ ] Request logging
[ ] Response timing
```

## Day 12 — Security + Rate Limiting

```text
[ ] Login rate limiting
[ ] Input validation review
[ ] Authorization review
[ ] JWT review
[ ] Refresh token review
[ ] Secret review
[ ] Sensitive logging review
[ ] Security review
```

Learn:

```text
Redis basics
rate limiting algorithms
distributed rate limiting
```

## Day 13 — Testing + Performance

```text
[ ] Authentication tests
[ ] Authorization tests
[ ] Project tests
[ ] Task tests
[ ] Comment tests
[ ] Notification tests
[ ] Validation tests
[ ] Error tests
[ ] Pagination tests
[ ] Statistics tests
[ ] Database indexes
[ ] Connection pooling review
```

## Day 14 — Advanced Python + Cleanup

```text
[ ] Review classes
[ ] Find one useful OOP use case
[ ] Review generators
[ ] Build one useful generator example
[ ] Review context managers
[ ] Review dataclasses
[ ] Review iterators
[ ] Review type hints
[ ] Refactor duplicated code
[ ] Clean project structure
[ ] README
[ ] Postman collection
[ ] Git cleanup
```

---

# 7-Day System Design Track

## Day 15 — Scaling

```text
[ ] Vertical scaling
[ ] Horizontal scaling
[ ] Load balancing
[ ] Stateless FastAPI
[ ] Uvicorn workers
[ ] Gunicorn concepts
[ ] Processes
[ ] Threads
[ ] Async
[ ] GIL
```

## Day 16 — Rate Limiting + Redis

```text
[ ] Fixed window
[ ] Sliding window
[ ] Token bucket
[ ] Redis counters
[ ] Distributed rate limiting
[ ] Login protection
```

## Day 17 — Caching

```text
[ ] Cache-aside
[ ] Cache hit/miss
[ ] TTL
[ ] Cache invalidation
[ ] Cache stampede
[ ] Redis
```

## Day 18 — Scheduler + Queues

```text
[ ] Cron
[ ] APScheduler
[ ] Scheduler vs worker
[ ] Queue
[ ] Producer
[ ] Consumer
[ ] Retry
[ ] Dead-letter queue
```

## Day 19 — Memory + Performance

```text
[ ] Python memory model
[ ] Reference counting
[ ] Garbage collection
[ ] Generators
[ ] Iterators
[ ] MongoDB cursors
[ ] Connection pooling
[ ] Profiling
```

## Day 20 — Reliability

```text
[ ] Timeouts
[ ] Retries
[ ] Exponential backoff
[ ] Jitter
[ ] Circuit breaker
[ ] Idempotency
[ ] Distributed locks
[ ] Graceful shutdown
[ ] Health checks
```

## Day 21 — System Design Interview

Draw and explain:

```text
                    Client
                      |
                      v
                Load Balancer
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
      FastAPI 1   FastAPI 2   FastAPI 3
          |           |           |
          +-----------+-----------+
                      |
             +--------+--------+
             |                 |
             v                 v
           Redis            MongoDB
             |
       +-----+------+
       |            |
       v            v
    Cache       Rate Limiter

                Queue
                  |
                  v
               Workers
                  |
                  v
             MongoDB / APIs

             Scheduler
                  |
                  v
                Queue
```

Be able to explain every component and why it exists.

---

# Interview Checklists

## Python

```text
What is a function?
When should you use a class?
What is OOP?
What is inheritance?
What is a decorator?
What is a generator?
What is an iterator?
What is a context manager?
What is a dataclass?
How does Python manage memory?
What is reference counting?
What is garbage collection?
What is the GIL?
Thread vs process?
When does async help?
CPU-bound vs I/O-bound?
```

## FastAPI

```text
How does FastAPI handle a request?
What is APIRouter?
What is Pydantic?
What are request/response models?
What is dependency injection?
What is Depends?
How do dependencies help authentication?
What is middleware?
How are exceptions handled?
How does FastAPI generate OpenAPI documentation?
What is async/await?
When should an endpoint be async?
How would you scale FastAPI?
```

## MongoDB

```text
How does MongoDB CRUD work?
What is ObjectId?
How do indexes work?
When should you use aggregation?
Embedding vs referencing?
How does pagination work?
How would you optimize a slow query?
What is connection pooling?
How would MongoDB handle high traffic?
What are transactions?
```

## System Design

```text
How would you handle 10,000 requests/second?
How does rate limiting work?
Why Redis?
How does distributed rate limiting work?
How does caching work?
How do you invalidate cache?
What is cache stampede?
How do background queues work?
Scheduler vs worker?
How do retries work?
What is exponential backoff?
What is a dead-letter queue?
What is idempotency?
What is a distributed lock?
What is a circuit breaker?
How do you handle external API failure?
How do you find a memory leak?
How do you monitor a backend?
How do you scale horizontally?
```

---

# Definition of Done

## Core

```text
[ ] User registration
[ ] User login
[ ] Access tokens
[ ] Refresh tokens
[ ] Logout/revocation
[ ] Authentication dependencies
[ ] Authorization
[ ] Projects
[ ] Project members
[ ] Tasks
[ ] Assignment
[ ] Status rules
[ ] Comments
[ ] Notifications
[ ] Search
[ ] Filtering
[ ] Sorting
[ ] Pagination
[ ] Statistics
[ ] Validation
[ ] Error handling
[ ] Logging
[ ] Tests
[ ] MongoDB indexes
[ ] README
[ ] Postman collection
[ ] Git history
```

## Advanced

```text
[ ] Rate limiting
[ ] Redis
[ ] Caching
[ ] Scheduler
[ ] Background workers
[ ] Queue concepts
[ ] Retry/backoff
[ ] Idempotency
[ ] Memory management
[ ] Connection pooling
[ ] Horizontal scaling
[ ] Load balancing
[ ] Health checks
[ ] Graceful shutdown
[ ] Observability
[ ] System design scenarios
```

---

# Daily Learning Method

Every day:

```text
1. Read today's requirements.
2. Learn only the listed prerequisite topics.
3. Use official documentation/reference.
4. Understand the concepts.
5. Design your approach.
6. Write the code yourself.
7. Test it.
8. Handle edge cases.
9. Refactor.
10. Commit to Git.
```

Do not immediately ask what code to write.

First ask:

```text
What should happen?
What data do I need?
What business rules exist?
What responsibilities are involved?
What functions/classes/dependencies should handle them?
```

Only then implement.

---

# Mentor Workflow

The assistant should guide rather than build the project.

```text
You:
"Day 4"

Assistant:
Today's goal
What to learn
Where to learn
Today's tasks
Done criteria

You:
Learn independently.

You:
"I don't understand refresh tokens."

Assistant:
Explain the concept.

You:
"I designed these functions. Is my design reasonable?"

Assistant:
Review the design.

You:
"Here is my code."

Assistant:
Review bugs/design problems without rewriting the whole project.
```

The project remains your code.

---

# Final Objective

At the end, you should be able to explain:

```text
I built a Python backend using FastAPI and MongoDB.

I designed the API and database myself.

I implemented JWT authentication and refresh tokens.

I used Pydantic for request/response validation.

I used FastAPI dependency injection for authentication and authorization.

I implemented MongoDB queries, indexes, aggregation and pagination.

I wrote automated tests using pytest.

I added logging, error handling and middleware.

I understand Redis for rate limiting and caching.

I understand background workers, queues and schedulers.

I understand memory management, async programming, scaling and reliability.

I can explain how I would scale the system for high traffic.
```

That is the actual goal of this roadmap.
