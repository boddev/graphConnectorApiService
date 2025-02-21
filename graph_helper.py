from msgraph import GraphServiceClient  # Import GraphServiceClient from msgraph
from azure.identity import ClientSecretCredential  # Import ClientSecretCredential from azure.identity
from fastapi import HTTPException  # Import HTTPException from fastapi
from msgraph.generated.models.external_connectors.external_connection import ExternalConnection  # Import ExternalConnection model
from schemas import demo_schema as schema  # Import demo_schema from schemas

# Initialize the Graph client
client_id = ''  # Client ID for Azure AD application
client_secret = ''  # Client secret for Azure AD application
tenant_id = ''  # Tenant ID for Azure AD application

# Create a credential object using client ID, client secret, and tenant ID
credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret
)

# Initialize the GraphServiceClient with the credential
graph_client = GraphServiceClient(credentials=credential)

# Define an asynchronous function to create an external connection
async def create_external_connection(connection_id, name, description):
    # Create an ExternalConnection object with the provided parameters
    connection = ExternalConnection(
        id=connection_id,
        name=name,
        description=description,
        state="ready"
    )
    try:
        # Send a POST request to create the external connection
        response = await graph_client.external.connections.post(body=connection)
    except Exception as e:
        # Print the error message and return an HTTPException with status code 500
        print(f"Error creating external connection: {e}")
        return HTTPException(status_code=500, detail=str(e))
    # Print a success message and return the response
    print("External connection created successfully")
    return response

# Define an asynchronous function to create a schema for the external connection
async def create_schema(connection_id):
    # Send a PATCH request to create the schema for the specified connection ID
    response = await graph_client.external.connections.by_external_connection_id(connection_id).schema.patch(schema)
    # Print a success message and return the response
    print('Schema created successfully')
    return response

# ...existing code...