from azure.storage.blob import BlobServiceClient
from graph_helper import graph_client
from msgraph.generated.models.external_connectors.external_item import ExternalItem
from msgraph.generated.models.external_connectors.acl import Acl
from msgraph.generated.models.external_connectors.acl_type import AclType
from msgraph.generated.models.external_connectors.access_type import AccessType
from msgraph.generated.models.external_connectors.properties import Properties
from msgraph.generated.models.external_connectors.external_item_content import ExternalItemContent
from msgraph.generated.models.external_connectors.external_item_content_type import ExternalItemContentType

# Initialize the BlobServiceClient
connection_string = ''
blob_service_client = BlobServiceClient.from_connection_string(connection_string)


async def get_blob_content(container_name):
    container_client = blob_service_client.get_container_client(container_name)
    blob_contents = []

    for blob in container_client.list_blobs():
        if blob.size <= 0:
            continue
        if len(blob_contents) >= 10:
            break
        blob_client = container_client.get_blob_client(blob)

        request_body = ExternalItem(
            acl = [
                Acl(
                    type = AclType.Everyone,
                    value = "everyone",
                    access_type = AccessType.Grant,
                )
            ],
            properties = Properties(
                additional_data = {
                    "Name":blob.name.split('/')[1],
                    "Description": "Some test data for description",
                    "FunFact": "Honey never spoils",
                    "url": blob_client.url,
                    "Content": "Some test data for content",
                }
            ),
            content = ExternalItemContent(
                value = blob_client.download_blob().readall().decode('utf-8'),
                type = ExternalItemContentType.Html,
            ),
        )
        externalItem_id = blob.name.split('/')[1].replace('.','').replace(' ','')#blob_client.container_name+"/"+blob_client.blob_name

        try:
            result = await graph_client.external.connections.by_external_connection_id('bodConnection').items.by_external_item_id(externalItem_id).put(request_body)
            print(result)
        except Exception as e:
            print(f"Error pushing content to Graph API: {e}")

    
    return blob_contents

# ...existing code...
