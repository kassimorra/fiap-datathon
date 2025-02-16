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
from feast.types import Float32, Float64, Int64, String
from feast.infra.offline_stores.contrib.postgres_offline_store.postgres_source import PostgreSQLSource

project = Project(name="feast", description="project to predict the next news")
globo = Entity(name="globo", join_keys=["userid"], value_type=ValueType.STRING)

globo_stats_source = PostgreSQLSource(
    name="globo_source",
    query="select * from table_full",
    timestamp_field="event_timestamp",
    created_timestamp_column="created",
)

globo_features_view = FeatureView(
    name="globo_features",
    entities=[globo],
    ttl=None,  # Set a time-to-live if needed
    schema=[
        Field(name="history", dtype=String),
        Field(name="numberofclickshistory", dtype=Int64),
    ],
    source=globo_stats_source
)