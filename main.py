from fastapi import FastAPI, HTTPException, Request  # Import FastAPI, HTTPException, and Request from FastAPI
from fastapi.responses import RedirectResponse  # Import RedirectResponse from FastAPI
from urllib3 import HTTPResponse  # Import HTTPResponse from urllib3
from graph_helper import create_external_connection, create_schema  # Import functions from graph_helper
from azure_blob_helper import get_blob_content  # Import function from azure_blob_helper
from graph_helper import client_id  # Import client_id from graph_helper

# Initialize the FastAPI app
app = FastAPI()

# Define a route to redirect to a URL for admin consent
@app.get("/redirect")
def redirect_to_url(tenant_id: str):
    url = f"https://login.microsoftonline.com/{tenant_id}/adminconsent?client_id={client_id}"  # Construct the URL for admin consent
    return RedirectResponse(url)  # Redirect to the constructed URL

# Define a route to create an external connection
@app.post("/create-connection")
async def create_connection(request: Request):
    try:
        body = await request.json()  # Parse the request body as JSON

        response = await create_external_connection(body['connection_id'], body['name'], body['description'])  # Call the create_external_connection function
        print("External connection created successfully")  # Print a success message
        return response  # Return the response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Raise an HTTPException with status code 500 and the error message

# Define a route to create a schema
@app.post("/create-schema")
async def create_schema_endpoint(request: Request):
    try:
        body = await request.json()  # Parse the request body as JSON
        response = await create_schema(body['connection_id'])  # Call the create_schema function
        return response  # Return the response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Raise an HTTPException with status code 500 and the error message

# Define a route to push content from Azure Blob storage to the Graph Data Connection
@app.post("/push-content")
async def push_content(request: Request):
    try:
        body = await request.json()  # Parse the request body as JSON
        content = await get_blob_content(body['container_name'], body['connection_id'])  # Call the get_blob_content function
        return HTTPResponse(status_code=200)  # Return an HTTPResponse with status code 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Raise an HTTPException with status code 500 and the error message