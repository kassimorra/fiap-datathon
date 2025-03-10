from datetime import timedelta
import pandas as pd
from feast import (
    Entity,
    ValueType,
    FeatureService,
    FeatureView,
    Field,
    FileSource,
    Project,
    PushSource,
    RequestSource,
)
from feast.on_demand_feature_view import on_demand_feature_view
from feast.types import Float32, Float64, Int64, String, UnixTimestamp
from feast.infra.offline_stores.contrib.postgres_offline_store.postgres_source import PostgreSQLSource

project = Project(name="globo_feature", description="project to predict the next news")

globo = Entity(
    name="globo", 
    join_keys=["userid"], 
    value_type=ValueType.STRING, 
    description="ID of the user"
)

globo_source = PostgreSQLSource(
    name="globo_source",
    query="select userid, news_concat, history, timestamphistory from table_full",
    timestamp_field="timestamphistory",
#   created_timestamp_column="create_timestamp",
)

globo_fv = FeatureView(
    name="globo_fv",
    entities=[globo],
    ttl=None,
    schema=[
        Field(name="timestamphistory", dtype=UnixTimestamp),
        Field(name="history", dtype=String),
        Field(name="news_concat", dtype=String),
    ],
    source=globo_source,
    online=True,
    tags={},
)

