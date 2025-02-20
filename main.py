from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from graph_helper import create_external_connection, create_schema
#from azure_blob_helper import get_blob_content, push_content_to_external_connection
from graph_helper import client_id
from msgraph import GraphServiceClient
#from msal import ConfidentialClientApplication
from azure.identity import ClientSecretCredential
from msgraph.generated.models.external_connectors.external_connection import ExternalConnection

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
def create_schema_endpoint(connection_id: str, schema: dict):
    try:
        response = create_schema(connection_id, schema)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @app.post("/push-content")
# def push_content(connection_id: str, container_name: str, blob_name: str):
#     try:
#         content = get_blob_content(container_name, blob_name)
#         response = push_content_to_external_connection(connection_id, content)
#         return response
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))