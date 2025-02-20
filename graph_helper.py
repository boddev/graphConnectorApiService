from msgraph import GraphServiceClient
from msal import ConfidentialClientApplication
from msgraph.generated.models.external_connectors.external_connection import ExternalConnection
from msgraph.generated.models.external_connectors.schema import Schema
from msgraph.generated.models.external_connectors.property_ import Property_
from msgraph.generated.models.external_connectors.property_type import PropertyType
from msgraph.generated.models.external_connectors.label import Label

# Initialize the Graph client
client_id = ''
client_secret = ''
tenant_id = ''

app = ConfidentialClientApplication(
    client_id,
    authority=f'https://login.microsoftonline.com/{tenant_id}',#'https://login.microsoftonline.com/common'
    client_credential=client_secret
)

token = app.acquire_token_for_client(scopes=['https://graph.microsoft.com/.default'])

graph_client = GraphServiceClient(credentials=token['access_token'])

async def create_external_connection(connection_id, name, description):

    connection = ExternalConnection(
        id=connection_id,
        name=name,
        description=description,
        state='draft'
    )
    response = await graph_client.external.connections.post(body=connection)
    print("External connection created successfully")
    return response


async def create_schema(connection_id):
    schema = Schema(
        base_type="microsoft.graph.externalItem",
        properties=[
            Property_(
                name="Name",
                type=PropertyType.String,
                is_queryable=True,
                is_searchable=True,
                is_retrievable=True,
                labels=[
                    Label.Title
                ]
            ),
            Property_(
                name="Description",
                type=PropertyType.String,
                is_queryable=True,
                is_searchable=True,
                is_retrievable=True
            ),
            Property_(
                name="FunFact",
                type=PropertyType.String,
                is_retrievable=True
            ),
            Property_(
                name="url",
                type=PropertyType.String,
                is_retrievable=True,
                labels=[
                    Label.Url
                ]
            )
        ]
    )
    graph_client.external.connections
    response = await graph_client.external.connections.by_external_connection_id(connection_id).schema.patch(schema)
    print('Schema created successfully')
    return response

# ...existing code...