from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from urllib3 import HTTPResponse
from graph_helper import create_external_connection, create_schema
from azure_blob_helper import get_blob_content
from graph_helper import client_id

app = FastAPI()

@app.get("/redirect")
def redirect_to_url(tenant_id: str):
    url = f"https://login.microsoftonline.com/{tenant_id}/adminconsent?client_id={client_id}"
    return RedirectResponse(url)

@app.post("/create-connection")
async def create_connection(request: Request):
    try:
        body = await request.json()

        response = await create_external_connection(body['connection_id'], body['name'], body['description'])
        print("External connection created successfully")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create-schema")
async def create_schema_endpoint(request: Request):
    try:
        body = await request.json()
        response = await create_schema(body['connection_id'])
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/push-content")
async def push_content(request: Request):
    try:
        body = await request.json()
        content = await get_blob_content(body['container_name'])
        return HTTPResponse(status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))