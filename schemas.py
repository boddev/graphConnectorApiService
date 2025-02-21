from msgraph.generated.models.external_connectors.schema import Schema
from msgraph.generated.models.external_connectors.property_ import Property_
from msgraph.generated.models.external_connectors.property_type import PropertyType
from msgraph.generated.models.external_connectors.label import Label

demo_schema = Schema(
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
            ),
            Property_(
                name="Content",
                type=PropertyType.String,
                is_retrievable=True,
                labels=[
                    
                ]
            )
        ]
    )