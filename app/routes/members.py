from fastapi import APIRouter, Depends, Request
from app.dependencies.dependencies import verify_token
from app.exceptions.serialiaze import serialize_doc
from app.exceptions.response import success, error
from app.database.connection import db
from bson import ObjectId


router =  APIRouter(prefix="/project", tags=['/members'])


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


"""
1. Get current user from JWT
2. Find the project
3. If project doesn't exist → 404
4. Check current user is owner OR member
5. If neither → 403
6. Get the users from the members array
7. Return member details
"""

@router.get("/{project_id}/members", response_model=dict)
async def get_project_members(project_id : str, auth=Depends(verify_token)):
    try:
        user_id = auth['sub']
        user_object_id =  ObjectId(user_id)
        pro_col = db['projects']
        pipeline = [
            {"$match" : {
                "_id" : ObjectId(project_id)
            }},
            {"$lookup" : {
                "from" : "users",
                "localField" : "members",
                "foreignField" : "_id",
                "as" : "user"
            }},
            # {
            #     "$unwind" : "$user"
            # }
          
        ]
        result = list(pro_col.aggregate(pipeline))
        if len(result) == 0:
            return error(404, "Project Not found")
        elif result[0]['owner_id'] != user_object_id and user_object_id not in result[0]['members']:
            return error(403, "User must be a member or owner of the project!")

        return success(200, "success", serialize_doc(result))
    except Exception as e:
        return error(500, str(e))


"""
1. Get current user from JWT
        ↓
2. Get project_id from URL
        ↓
3. Get member_id/user_id from URL
        ↓
4. Find project
        ↓
   Project doesn't exist → 404
        ↓
5. Check current user is the project owner
        ↓
   Not owner → 403
        ↓
6. Check the user is actually a member
        ↓
   Not a member → 404
        ↓
7. Check the target user is NOT the owner
        ↓
   Owner → ❌ Don't allow removal
        ↓
8. Remove user from members array
        ↓
9. Success"""

@router.delete("/{project_id}/members/{member_id}", response_model=dict)
def remove_member(req : Request, auth=Depends(verify_token)):
    try:
        curr_user_id = auth['sub']
        curr_user_object_id = ObjectId(curr_user_id)
        project_id = req.path_params.get('project_id')
        member_id = req.path_params.get("member_id")

        pro_col = db['projects']
        pro_det =  pro_col.find_one({"_id" : ObjectId(project_id)})

        if not pro_det:
            return error(404, "project not found!")
        elif pro_det['owner_id'] != curr_user_object_id:
            return error(403, "This action can only performed by the Owner of the project!")
        elif ObjectId(member_id) not in pro_det['members']:
            return error(409, "This user is not a member of this project!")

        result =  pro_col.update_one({"_id" : ObjectId(project_id)}, {"$pull" : {"members" : ObjectId(member_id)}})

        return success(200, "Member Removed successfully!", result.modified_count)
    except Exception as e:
        return error(500, f"Internal Server Error: {e}")