import streamlit as st
import pandas as pd
from app.crawlers import youtube
from app.crawlers import reddit

st.set_page_config(page_title = "Social Listening Dashboard", layout = "wide")
st.title("Social Listening Dashboard")

with st.sidebar:
    st.header("Settings")
    
    st.subheader("Reddit", divider = "grey")
    subreddit = st.text_input("Subreddit Name", placeholder = "search...")
    limit = st.slider("Number of Posts", min_value = 1, max_value = 10, value = 5)
    
    st.subheader("YouTube", divider = "grey")

if subreddit.strip():
    with st.spinner("Fetching posts from Reddit..."):
        try:
            dfs = reddit.search_subreddit(subreddit, limit)
            df = dfs["posts_df"]

            # Convert timestamp to readable date
            df["post_created_utc"] = pd.to_datetime(df["post_created_utc"], unit="s")

            # Display basic table
            st.subheader(f"Latest Posts from r/{subreddit}")
            st.dataframe(df[[
                "post_title", "post_upvotes", "post_upvote_ratio", 
                "post_number_of_comments", "post_created_utc", "post_permalink"
            ]])

        except Exception as e:
            st.error(f"Failed to load data: {e}")
else:
    st.info("Enter a subreddit name to begin.")