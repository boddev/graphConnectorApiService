from azure.storage.blob import BlobServiceClient
from main import graph_client

# Initialize the BlobServiceClient
connection_string = 'YOUR_AZURE_STORAGE_CONNECTION_STRING'
blob_service_client = BlobServiceClient.from_connection_string(connection_string)


def get_blob_content(container_name, blob_name):
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)
    blob_content = blob_client.download_blob().readall()
    return blob_content


def push_content_to_external_connection(connection_id, content):
    url = f'https://graph.microsoft.com/v1.0/external/connections/{connection_id}/items'
    response = graph_client.post(url, json=content)
    return response.json()

# ...existing code...
