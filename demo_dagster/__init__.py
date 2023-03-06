from dagster import Definitions

from demo_dagster.hello_dagster import hackernews_top_stories, hackernews_top_story_ids
from demo_dagster.my_pipeline import my_job

defs = Definitions(
    assets=[hackernews_top_story_ids, hackernews_top_stories],
    jobs=[my_job]
)
