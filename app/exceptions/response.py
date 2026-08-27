from fastapi.responses import JSONResponse

def success(st_code: int, mes: str = None, data=None):
    resp = {"status": "success"}
    if mes: resp["message"] = mes
    if data: resp["data"] = data
    return JSONResponse(status_code=st_code, content=resp)


def error(st_code : int, mes : str):
    print(f"Error: {mes}")
    return JSONResponse(
        status_code=st_code,
        content={
            "status" : "error",
            "message" : mes
        }
    )