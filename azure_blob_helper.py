from azure.storage.blob import BlobServiceClient  # Import BlobServiceClient from azure.storage.blob
from graph_helper import graph_client  # Import graph_client from graph_helper
from msgraph.generated.models.external_connectors.external_item import ExternalItem  # Import ExternalItem model
from msgraph.generated.models.external_connectors.acl import Acl  # Import Acl model
from msgraph.generated.models.external_connectors.acl_type import AclType  # Import AclType model
from msgraph.generated.models.external_connectors.access_type import AccessType  # Import AccessType model
from msgraph.generated.models.external_connectors.properties import Properties  # Import Properties model
from msgraph.generated.models.external_connectors.external_item_content import ExternalItemContent  # Import ExternalItemContent model
from msgraph.generated.models.external_connectors.external_item_content_type import ExternalItemContentType  # Import ExternalItemContentType model

# Initialize the BlobServiceClient
connection_string = ''  # Azure Blob Storage connection string
blob_service_client = BlobServiceClient.from_connection_string(connection_string)  # Create BlobServiceClient instance

# Define an asynchronous function to get blob content from a container
async def get_blob_content(container_name, container_id):
    container_client = blob_service_client.get_container_client(container_name)  # Get the container client
    blob_contents = []  # Initialize an empty list to store blob contents

    # Iterate through the blobs in the container
    for blob in container_client.list_blobs():
        if blob.size <= 0:  # Skip empty blobs
            continue
        if len(blob_contents) >= 10:  # Limit the number of blobs processed to 10
            break
        blob_client = container_client.get_blob_client(blob)  # Get the blob client

        # Create the request body for the external item
        request_body = ExternalItem(
            acl=[
                Acl(
                    type=AclType.Everyone,  # Set ACL type to Everyone
                    value="everyone",  # Set ACL value to "everyone"
                    access_type=AccessType.Grant,  # Set access type to Grant
                )
            ],
            properties=Properties(
                additional_data={
                    "Name": blob.name.split('/')[1],  # Set the Name property
                    "Description": "Some test data for description",  # Set the Description property
                    "FunFact": "Honey never spoils",  # Set the FunFact property
                    "url": blob_client.url,  # Set the URL property
                    "Content": "Some test data for content",  # Set the Content property
                }
            ),
            content=ExternalItemContent(
                value=blob_client.download_blob().readall().decode('utf-8'),  # Download and decode the blob content
                type=ExternalItemContentType.Html,  # Set the content type to HTML
            ),
        )
        externalItem_id = blob.name.split('/')[1].replace('.', '').replace(' ', '')  # Generate the external item ID

        try:
            # Push the content to the Graph API
            result = await graph_client.external.connections.by_external_connection_id(container_id).items.by_external_item_id(externalItem_id).put(request_body)
            print(result)  # Print the result
        except Exception as e:
            print(f"Error pushing content to Graph API: {e}")  # Print the error message

    return blob_contents  # Return the list of blob contents

# ...existing code...
