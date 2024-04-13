import random
import time

import praw
import os, shutil, pathlib
import json

reddit = praw.Reddit(
    client_id="s9OQw96pTwsDMmr2_MUUqg",
    client_secret="319sCgCY0EYvKo3UEjFkgsoxVlXeQw",
    user_agent="app by u/UPatel8829",
)

# [
#     "AskReddit", "funny", "gaming", "Aww", "todayilearned",
#     "mildlyinteresting", "Showerthoughts", "memes", "pics", "IAmA",
#     "explainlikeimfive", "science", "worldnews", "movies", "videos",
#     "Music", "DIY", "LifeProTips", "food", "books",
#     "GetMotivated", "Art", "history", "gadgets", "travel",
#     "EarthPorn", "space", "dataisbeautiful", "Futurology", "Documentaries",
#     "sports", "UpliftingNews", "nosleep", "WritingPrompts", "tifu",
#     "personalfinance", "learnprogramming", "TwoXChromosomes", "nottheonion",
#     "photoshopbattles", "pokemon", "NintendoSwitch", "CozyPlaces", "rarepuppers",
#     "wholesomememes", "OldSchoolCool", "HumansBeingBros", "MadeMeSmile",
#     "AnimalsBeingDerps", "Unexpected"
# ]

subreddits_name = [
    "datascience",
    "PersonalFinanceCanada",
    "personalfinance",
    "WritingPrompts",
    "lifehacks",
    "travel",
    "politics",
    "programming",
    "YouShouldKnow",
    "ChatGPT",
    "entertainment",
    "dating_advice",
    "Entrepreneur",
    "careerguidance", "careeradvice", "technology", "writing", "Poem", "realestateinvesting", "RealEstate"
                                                                                              "news",
    "interviewpreparations",
    "jobsearchhacks",
    "Resume",
    "jobs",
    "skills"
]

jsons = os.listdir("./data")
print(jsons)


def get_comments(subreddit):
    comment_fetched = 0
    sub_reddit = reddit.subreddit(subreddit)
    tops = sub_reddit.top()

    for submission in tops:
        if not submission.stickied and f"{submission.id}.json" not in jsons and submission.num_comments > 50:
            json_submission = {
                'title': submission.title,
                'id': submission.id,
                'create_at': submission.created_utc,
                'score': submission.score,
            }

            comments = []
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                if comment.body:
                    comment_obj = {
                        'id': comment.id,
                        'parent': comment.parent_id,
                        'ans': comment.body,
                        'score': comment.score,
                    }
                    if not comment.is_root:
                        parent_text = get_parent_body(comment.parent_id)
                        print(comment.parent_id)
                        print("|---", comment.id)
                        comment_obj["que"] = parent_text
                        comment_fetched += 1
                        comments.append(comment_obj)
                        print(f"No. comments: {comment_fetched} ({len(os.listdir('./data'))})")

            json_submission['comments'] = comments
            with open(f"data/{submission.id}.json", "w") as outfile:
                json.dump(json_submission, outfile, indent=4)


def get_parent_body(id):
    time.sleep(random.randint(1, 3))
    comment = reddit.comment(id)
    return comment.body


completed = []


def start_extraction():
    for subreddit in subreddits_name:
        get_comments(subreddit)
        print("Ongoing: ====================>>>>>", subreddit)
        completed.append(subreddit)
        time.sleep(10)


try:
    start_extraction()
except Exception as e:
    print(e)
    time.sleep(100)
    start_extraction()
