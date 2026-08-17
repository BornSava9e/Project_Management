* Day 1
1. setup venv using "python -m venv venv" then activate using ".venv\scripts\activate"
# Python venv is a built‑in tool that creates a virtual environment — an isolated workspace with its own Python interpreter and libraries, preventing dependency conflicts between projects.

2. upgrade pip using "python -m pip install --upgrade pip"
3. install fast api  using python -m pip install fastapi
4. we use python -m for installing the compatible version according to our system.
5. install uvicorn using pip install uvicorn
# Uvicorn is a lightning‑fast ASGI (Asynchronous Server Gateway Interface) web server for Python that runs asynchronous frameworks like FastAPI and Starlette, supporting HTTP and WebSockets. It’s lightweight, fast, and commonly used in modern web app deployments. Need uvicorn because fastapi framework don't serve requests on their own. they rely on an ASGI Server like Uvicorn to handle incoming HTTP/Websocket connections and route them to your app.

6. install pydantic using "pip install pydantic"
# Pydantic is a Python library for data validation and type enforcement. It uses Python type hints to ensure data is correct and automatically converts types when possible. It’s especially popular in FastAPI for validating request and response models.

7. install pytest  using "pip install pytest"
# Pytest is a Python testing framework that makes writing and running tests simple. It supports fixtures, plugins, and automatic test discovery, and is widely used for both small projects and large applications. It ensures code reliability by catching bugs early, encourages test driven development.

8. install python-dotenv using "pip install python-dotenv"
9. install json web token using "pip install jsonwebtoken"
# used for authentication and authorization, stateless session - no need to store session information, instead jwt contain all the infromation in encoded form.
10. created requirement file using pip freeze > requiremnt.txt

11. install pymongo for using mongodb

12. create a basic app of fast api


* Day 2 
13. created seperate route name users.py in routes folder and map it main.py and added a error handling thing for the _id field it is giving a serialization error.
# In FastAPI, APIRouter is used to organize routes into separate modules. It allows you to group endpoints with a common prefix and tags, making large applications modular and easier to maintain. You register routers in main.py using app.include_router().
# FastAPI uses routes to define how the application responds to HTTP requests. Each route maps a URL path and method (GET, POST, etc.) to a function. This makes the app modular, RESTful, and automatically documented.

# Routers are connected to the main FastAPI app using app.include_router(). The prefix adds a common path prefix to all routes in the router, while tags group those routes in the auto‑generated API docs for better organization.


14. pydantic scheams are used for validation of request body check its datatypes and convert body to json automatically so getting less error for serialization.
# Benefits - Type safety → IDE autocompletion and fewer runtime errors. Automatic validation → No manual checks needed.  Cleaner code → Less boilerplate.   OpenAPI integration → Docs are generated automatically.
# Pydantic schemas in FastAPI are Python classes that define and validate the structure of request and response data. They ensure type safety, automatic validation, and generate OpenAPI documentation. Typically, you use separate schemas for input and output to keep APIs secure and clean.


15. have built a pydantic basic schema for getting the users from database make it handle _id field and datetime by importing some modules. now only the fields mention in the schema are returned as output for the api.

16. created a settings.py file for storing all the credentials and global variables.

17. No hardcoded secrets because it have sercurity risk, environment differences, compliance issues fear of leaking secrets, Maintainability hard to maintain them for multiple users.

18. added prefix for the user.router in main.md file for now "/api/v1" is the prefix for the user api's.

19. added try except hanlding in the Get user api in user.py.

20. See the swagger by running the server watched it on "localhost:3000/docs" link right now there is 2 api's which is correct.