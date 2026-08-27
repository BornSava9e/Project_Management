from fastapi import APIRouter, Depends, Request
from app.dependencies.dependencies import verify_token
from app.exceptions.serialiaze import serialize_doc
from app.exceptions.response import success, error
from app.database.connection import db
from bson import ObjectId


router =  APIRouter(prefix="/project", tags=['/members'])

"""1. Get current user from JWT
2. Get project_id from URL
3. Get user_id to add from request body
4. Check project exists
5. Check current user is the project owner
6. Check the user being added exists
7. Check they are not already in members
8. Add them using $addToSet
9. Return success"""

@router.post("/{project_id}/members", response_model=dict)
async def add_member(req : Request, auth=Depends(verify_token)):
    try:
        user_id = auth['sub']
        body = await req.json()
        project_id = req.path_params.get('project_id')
        member_id = body.get('member_id')

        if not member_id:
            return error(400, "Please provide member id!")
        member_object_id = ObjectId(member_id)

        pro_col = db['projects']
        user_col =  db['users']
        check_user =  user_col.find_one({"_id": ObjectId(member_id)})
        check_project= pro_col.find_one({"_id" : ObjectId(project_id)})

        if not check_project:
            return error(404, "project not found")
        elif check_project['owner_id'] != ObjectId(user_id):
            return error(403, "you are not authorized to perform this action!")
        elif not check_user:
            return error(404, "Memeber not found")
        elif member_object_id in check_project['members']:
            return error(409, "user is already a memeber in this project!")
        else:
            print("projec found")

        pro_col.update_one({"_id" : ObjectId(project_id)}, {"$addToSet" : {"members" : member_object_id}})
        
        return success(200, "Memeber Added Successfully!")
    except Exception as e:
        return error(500, str(e))


@router.get("/{project_id}/memebser", response_model=dict)
def get_project_members(project_id : str, auth=Depends(verify_token)):
    try:
        return success(200, "success", [])
    except Exception as e:
        return error(500, str(e))