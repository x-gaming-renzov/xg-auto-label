from langgraph.graph import StateGraph, START, END

import os, pathlib, json, dotenv
from termcolor import colored

from .nodes.nodes import *
from .states.states import *

dotenv.load_dotenv()

def get_graph():
    graph = StateGraph(GenerateRedditDataState)

    graph.add_node("generate_reddit_data", generate_reddit_data)
    graph.add_node("generate_reddit_comments_from_subreddit", generate_reddit_comments_from_subreddit)
    graph.add_node("generate_relevance", generate_relevance)
    graph.add_node("generate_task_info", generate_task_info)

    graph.add_edge(START, "generate_reddit_data")
    graph.add_edge("generate_reddit_data", "generate_reddit_comments_from_subreddit")
    graph.add_edge("generate_reddit_comments_from_subreddit", "generate_relevance")
    graph.add_edge("generate_relevance", "generate_task_info")
    graph.add_edge("generate_task_info", END)

    compiled_graph = graph.compile()

    return compiled_graph

def run(user_id, subreddits, kb_data, reddit_client_id, reddit_client_secret, reddit_user_agent, cache_path = "/cache"):
    cache_path = os.getcwd() + "/" + cache_path + "/generate_reddit_data"
    if not os.path.exists(cache_path):
        os.makedirs(cache_path)
    graph = get_graph()
    final_state = graph.invoke({
        "subreddits": subreddits,
        "kb_data": kb_data,
        "cache_path": cache_path,
        "reddit_client_id": reddit_client_id,
        "reddit_client_secret": reddit_client_secret,
        "reddit_user_agent": reddit_user_agent,
        "user_id": user_id
    })
    return final_state