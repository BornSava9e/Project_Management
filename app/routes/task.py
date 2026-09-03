from fastapi import APIRouter, Depends, Request
from app.database.connection import db
from app.schema.taskSchema import CreateTask
import datetime
from app.dependencies.dependencies import verify_token
from app.exceptions.response import success, error
from app.exceptions.serialiaze import serialize_doc
from bson import ObjectId

router = APIRouter(prefix="/task", tags=['task'])

"""
1. Get current user from JWT
        ↓
2. Convert project_id to ObjectId
        ↓
3. Find project
        ↓
4. Check project exists → 404
        ↓
5. Check current user is owner/member
        ↓
   No → 403
        ↓
6. If assigned_to exists:
      - Check user exists
      - Check user is a project member
        ↓
7. Create task document
        ↓
8. Store in tasks collection
        ↓
9. Return created task



payload = {
    "project_id": ObjectId(project_id),
    "title": body.title,
    "description": body.description,
    "created_by": ObjectId(auth["sub"]),
    "assigned_to": ObjectId(body.assigned_to) if body.assigned_to else None,
    "status": body.status.value,
    "priority": body.priority,
    "due_date": body.due_date,
    "tags": body.tags or [],
    "created_at": datetime.now(),
    "updated_at": None,
    "completed_at": None
}"""




@router.post('/{project_id}', response_model=dict)
async def create_task(project_id :str, body:CreateTask, auth=Depends(verify_token)):
    try:
        user_id = ObjectId(auth['sub'])
        project_object_id = ObjectId(project_id)


        pro_col = db['projects']
        pro_det =  pro_col.find_one({"_id" : project_object_id })  
        user_col = db['users']
        ass_user_check =  None
        if not pro_det: 
            return error(404, "Project Not Found!")
        elif pro_det["owner_id"] != user_id and user_id not in pro_det["members"]:
            return error(403, "User is not the owner or member in this project!")
        elif body.assigned_to:
            ass_user_check = user_col.find_one({"_id" : ObjectId(body.assigned_to)})
            if not ass_user_check:
                return error(404, "Member is not found can't be assigned to a project!")
            elif ObjectId(body.assigned_to) != pro_det["owner_id"] and ObjectId(body.assigned_to) not in pro_det["members"]: 
                return error(409, "Unable to assign task to this member!")
        else:
            print('All Condition Met!')

        payload = {
            "project_id": project_object_id,
            "title": body.title,
            "description": body.description,
            "created_by": user_id,
            "assigned_to": ObjectId(body.assigned_to) if body.assigned_to else None,
            "status": body.status.value,
            "priority": body.priority.value,
            "due_date": body.due_date,
            "tags": body.tags or [],
            "created_at": datetime.now(),
            "updated_at": None,
            "completed_at": None
        }
        print(serialize_doc(payload))
        task_col = db["tasks"]

        insert_task = task_col.insert_one(payload)
        return success(201, "Task created sucessfully", serialize_doc(payload))
    
    except Exception as e:
        return error(500, f"Internal Server Error : {e}")


"""1. Authenticate user
        ↓
2. Get project_id
        ↓
3. Find project
        ↓
   Not found → 404
        ↓
4. Check current user is owner OR member
        ↓
   Not authorized → 403
        ↓
5. Find all tasks where project_id matches
        ↓
6. Serialize tasks
        ↓
7. Return tasks
"""
@router.get("/{project_id}", response_model=dict)
def get_all_task(proejct_id: str, auth=Depends(verify_token)):
    try:
        return success(200, "All Task List",[])
    except Exception as e:
        return error(500, f"Internal Server Error: {e}")