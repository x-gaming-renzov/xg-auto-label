from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class GenerateRedditDataState(BaseModel):
    subreddits: List[str] 
    kb_data : str
    cache_path: str
    reddit_client_id: str
    reddit_client_secret: str
    reddit_user_agent: str
    