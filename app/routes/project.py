from fastapi import APIRouter, Depends, status, Request, HTTPException, Body
from app.database.connection import db
from app.config.settings import Settings
from fastapi.responses import JSONResponse
from app.schema.projectSchema import CreateProject
import datetime
from app.dependencies.dependencies import verify_token
from bson import ObjectId
from app.exceptions.serialiaze import serialize_doc
from app.exceptions.response import success, error

router = APIRouter(prefix="/project", tags=['project'])

def fetch_user(q):
    try:
        collection =  db['users']
        data = collection.find_one(q)
        return data
    except Exception as e:
        return e
    
@router.post("/", response_model=dict)
def create_project(body: CreateProject, auth=Depends(verify_token)):
    try:
        print(type(str(auth["sub"])))
        payload = {
            "name" : body.name,
            "description" : body.description,
            "owner_id" : ObjectId(auth["sub"]),
            "members" : body.members,
            "status" : "active",
            "created_at" : int(datetime.datetime.now().timestamp()),
            "updated_at" : None
        }

        project_collection =  db['projects']
        project_collection.insert_one(payload)


        return JSONResponse(
            status_code=200,
            content={
                "status" : "success",
                "message" : "Project Created Successfully!"
            }
        )

    except Exception as e:
        print(f"Error : {e}")
        raise HTTPException(
            status_code=500,
            detail= f"Internal Server Error : {e}"
        )




@router.get("/", response_model=dict)
async def get_project(req: Request, auth=Depends(verify_token)):
    try:
        path =  req.path_params
        user_id = auth['sub']
        project_col = db['projects']
        if path:
            print(path.get("projectId"))
            project_id = path.get("projectId")
            project_check =  project_col.find_one({"$and" : [
                {"_id" : ObjectId(project_id)},
                {"$or" : [
                    {"owner_id" : ObjectId(user_id)},
                    {"members" : ObjectId(user_id)}
                ]}
            ]})

            if not project_check:
                return error(404, "Project not Found!")
            else:
                return success(200,"success",serialize_doc(project_check))

        
        projects =  project_col.find({"$or" : [{"owner_id" : ObjectId(user_id)} , {"members" : {"$in" : [ObjectId(user_id)]}}] })
        
        serialize_data =  [serialize_doc(p) for p in projects]

        return success(200, "success", serialize_data)
    except Exception as e:
        return error(500, str(e))



@router.get("/{project_id}", response_model=dict)
def getProject(project_id : str, auth=Depends(verify_token)):
    try:    
        user_id = auth['sub']
        project_col = db['projects']
        project_check =  project_col.find_one({"_id" : ObjectId(project_id)})
        
        if not project_check:
            return error(404, "Project not Found!")
        else:
            if project_check["owner_id"] != ObjectId(user_id) and ObjectId(user_id) not in project_check['members']:
                return error(403, "Not authorized to see this project!")


        return success(200, "success", serialize_doc(project_check))
    except Exception as e:
        return error(500, str(e))


@router.patch("/{project_id}", response_model=dict)
async def update_project_details(project_id : str, body : dict = Body(...), auth=Depends(verify_token)):
    try:
        user_id = ObjectId(auth['sub'])
        project_collection =  db['projects']

        project_check = project_collection.find_one({"_id" : ObjectId(project_id)})
        print(body)

        if not project_check:
            return error(404, "Project Not Found!")
        elif project_check['owner_id'] != user_id:
            return error(403, "Not Authorized to update the project details!")
        else:
            print('Project Found')

        f"""name
            description
            status
            updated_at"""   


        update_params = {
            "name": body.get("name", project_check["name"]),
            "description": body.get("description", project_check["description"]),
            "status": body.get("status", project_check["status"]),
            "updated_at": int(datetime.datetime.now().timestamp()),
        }

        result = project_collection.update_one({"_id" : ObjectId(project_id)},{"$set": update_params})
        print(result.modified_count)
        return success(200,"success",result.modified_count)
    except Exception as e:
        return error(500, str(e))


@router.delete("/{project_id}",response_model=dict)
async def delete_project(project_id : str, auth=Depends(verify_token)):
    try:
        user_id = auth['sub']
        pro_col =  db['projects']
        pro_det = pro_col.find_one({"_id": ObjectId(project_id)})

        if not pro_det:
            return error(404, "Project not found!")
        elif pro_det["owner_id"] != ObjectId(user_id):
            return error(403, "Not Allowed to delete the project!")
        else:
            print('Project found!')

        result = pro_col.delete_one({"_id": ObjectId(project_id)})
        return success(200, "Deleted Successfully", result.deleted_count)
    except Exception as e:
        return error(500, str(e))


