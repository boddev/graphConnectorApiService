from msgraph import GraphServiceClient
from azure.identity import ClientSecretCredential
from fastapi import HTTPException
from msgraph.generated.models.external_connectors.external_connection import ExternalConnection
from schemas import demo_schema as schema

# Initialize the Graph client
client_id = ''
client_secret = ''
tenant_id = ''

credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret
)

graph_client = GraphServiceClient(credentials=credential)

async def create_external_connection(connection_id, name, description):

    connection = ExternalConnection(
        id=connection_id,
        name=name,
        description=description,
        state="ready"
    )
    try:
        response = await graph_client.external.connections.post(body=connection)
    except Exception as e:
        print(f"Error creating external connection: {e}")
        return HTTPException(status_code=500, detail=str(e))
    print("External connection created successfully")
    return response


async def create_schema(connection_id):
    response = await graph_client.external.connections.by_external_connection_id(connection_id).schema.patch(schema)
    print('Schema created successfully')
    return response

# ...existing code...