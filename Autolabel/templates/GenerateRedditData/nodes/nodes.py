import os, pathlib, json, dotenv
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor, as_completed

from langchain_openai import ChatOpenAI

from ....loader.reddit.XGReddit import XGReddit
from ..states.states import *

dotenv.load_dotenv()

#algorithmic nodes

def generate_reddit_data(GenerateRedditDataState : GenerateRedditDataState) -> GenerateRedditDataState:
    print(colored("Generating Reddit Data", "green"))
    
    reddit = XGReddit(
        GenerateRedditDataState.reddit_client_id,
        GenerateRedditDataState.reddit_client_secret,
        GenerateRedditDataState.reddit_user_agent
    )

    subreddits = []
    print(colored("Searching for subreddits...", "green"))
    with ThreadPoolExecutor() as executor:
        futures = []
        for subreddit in GenerateRedditDataState.subreddits:
            print(colored(f"Searching for subreddits related to '{subreddit}'...", "yellow"))
            future = executor.submit(reddit.search_subreddits, subreddit, 1)
            futures.append(future)
        
        for future in as_completed(futures):
            subreddits.extend(future.result())
    
    print(colored(f"Found {len(subreddits)} subreddits", "green"))
    
    print(colored("Fetching posts...", "green"))
    for subreddit in subreddits:
        print(colored(f"Fetching top posts from r/{subreddit.display_name} of all time", "yellow"))
        posts_all = subreddit.top(limit=20, time_filter="all")
        print(colored(f"Fetching top posts from r/{subreddit.display_name} of the week", "yellow"))
        posts_week = subreddit.top(limit=20, time_filter="week")
        print(colored(f"Fetching top posts from r/{subreddit.display_name} of the month", "yellow"))
        posts_month = subreddit.top(limit=20, time_filter="month")

        posts = []
        for post in posts_all:
            posts.append({
                "title": post.title,
                "post_id": post.id,
                "url": post.url,
                "text": post.selftext,
                "num_comments": post.num_comments,
                "upvotes": post.ups
            })
        for post in posts_week:
            posts.append({
                "title": post.title,
                "post_id": post.id,
                "url": post.url,
                "text": post.selftext,
                "num_comments": post.num_comments,
                "upvotes": post.ups
            })
        for post in posts_month:
            posts.append({
                "title": post.title,
                "post_id": post.id,
                "url": post.url,
                "text": post.selftext,
                "num_comments": post.num_comments,
                "upvotes": post.ups
            })

        # Save the posts to a file
        cache_path = GenerateRedditDataState.cache_path
        subreddit_path = os.path.join(cache_path, f"{subreddit.display_name}/posts.json")

        # Create the directory if it doesn't exist
        pathlib.Path(os.path.dirname(subreddit_path)).mkdir(parents=True, exist_ok=True)

        with open(subreddit_path, "w") as f:
            json.dump(posts, f, indent=4)
        
        print(colored(f"Saved {len(posts)} posts to {subreddit_path}", "green"))

    print(colored("Reddit data generation complete", "green"))
    return GenerateRedditDataState
              