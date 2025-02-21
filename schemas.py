from msgraph.generated.models.external_connectors.schema import Schema
from msgraph.generated.models.external_connectors.property_ import Property_
from msgraph.generated.models.external_connectors.property_type import PropertyType
from msgraph.generated.models.external_connectors.label import Label

# Define a schema for the external connection
demo_schema = Schema(
    base_type="microsoft.graph.externalItem",  # Base type for the schema
    properties=[
        Property_(
            name="Name",  # Name of the property
            type=PropertyType.String,  # Type of the property
            is_queryable=True,  # Indicates if the property can be queried
            is_searchable=True,  # Indicates if the property can be searched
            is_retrievable=True,  # Indicates if the property can be retrieved
            labels=[
                Label.Title  # Label for the property
            ]
        ),
        Property_(
            name="Description",  # Name of the property
            type=PropertyType.String,  # Type of the property
            is_queryable=True,  # Indicates if the property can be queried
            is_searchable=True,  # Indicates if the property can be searched
            is_retrievable=True  # Indicates if the property can be retrieved
        ),
        Property_(
            name="FunFact",  # Name of the property
            type=PropertyType.String,  # Type of the property
            is_retrievable=True  # Indicates if the property can be retrieved
        ),
        Property_(
            name="url",  # Name of the property
            type=PropertyType.String,  # Type of the property
            is_retrievable=True,  # Indicates if the property can be retrieved
            labels=[
                Label.Url  # Label for the property
            ]
        ),
        Property_(
            name="IconUrl",  # Name of the property
            type=PropertyType.String,  # Type of the property
            is_retrievable=True,  # Indicates if the property can be retrieved
            labels=[
                Label.IconUrl  # Label for the property
            ]
        )
    ]
)