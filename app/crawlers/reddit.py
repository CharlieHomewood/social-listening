# %%
import praw
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv(dotenv_path = ".env")

reddit = praw.Reddit(
    client_id = os.getenv("REDDIT_CLIENT_ID"),
    client_secret = os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent = os.getenv("REDDIT_USER_AGENT")
)

def search_subreddit(subreddit_name: str, post_limit: int):
    
    subreddit = reddit.subreddit(subreddit_name)
    
    subreddit_data = []
    subreddit_data.append({
        "subreddit_name": subreddit.display_name,
        "subreddit_id": subreddit.id,
        "subreddit_subscriber_count": subreddit.subscribers,
        "subreddit_description": subreddit.description
    })
    
    post_data = []
    for post in subreddit.new(limit = post_limit):
        post.comments.replace_more(limit = 1)
        post_data.append({
            "subreddit_name": subreddit_name,
            "subreddit_id": post.subreddit_id,
            "post_id": post.id,
            "post_permalink": post.permalink,
            "post_title": post.title,
            "post_upvotes": post.score,
            "post_upvote_ratio": post.upvote_ratio,
            "post_attached_url": post.url,
            "post_created_utc": post.created_utc,
            "post_number_of_comments": post.num_comments,
            "post_selftext": post.selftext
        })

    comments_data = []
    for comment in post.comments.list():
        comments_data.append({
            "subreddit_name": subreddit_name,
            "subreddit_id": comment.subreddit_id,
            "post_id": post.id,
            "comment_id": comment.id,
            "comment_permalink": comment.permalink,
            "comment_score": comment.score,
            "comment_body": comment.body
        })
        
    dfs = {
        "subreddit_summary_df": pd.DataFrame(subreddit_data),
        "posts_df": pd.DataFrame(post_data),
        "comments_df": pd.DataFrame(comments_data)
    }
    
    return dfs
# %%
search_subreddit("python", post_limit = 1)
# %%
