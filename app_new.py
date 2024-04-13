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

subreddits_name =[
    "photography",
    "Random_Acts_Of_Pizza",
    "battlestations",
    "minimalism",
    "buildapc",
    "Frugal",
    "malelivingspace",
    "Eyebleach",
    "thalassophobia",
    "itookapicture",
    "PerfectTiming",
    "quityourbullshit"
]

# subreddits_name = [
#     "PersonalFinanceCanada",
#     "personalfinance",
#     "WritingPrompts",
#     "lifehacks",
#     "travel",
#     "politics",
#     "programming",
#     "YouShouldKnow",
#     "ChatGPT",
#     "entertainment",
#     "dating_advice",
#     "Entrepreneur",
#     "careerguidance", "careeradvice", "technology", "writing", "Poem", "realestateinvesting", "RealEstate"
#                                                                                               "news",
#     "interviewpreparations",
#     "jobsearchhacks",
#     "Resume",
#     "jobs",
#     "skills"
# ]

jsons = os.listdir("./data")
print(jsons)


def get_comments(subreddit):
    comment_fetched = 0
    sub_reddit = reddit.subreddit(subreddit)
    tops = sub_reddit.top()

    for submission in tops:
        json_submission = {}
        comments = []
        try:
            if not submission.stickied and f"{submission.id}.json" not in jsons and submission.num_comments > 50:
                json_submission['title'] = submission.title
                json_submission['id'] = submission.id
                json_submission['create_at'] = submission.created_utc
                json_submission['score'] = submission.score

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
        except Exception as e:
            print(e)
            start_extraction()
        finally:
            print("Saving json...")
            json_submission['comments'] = comments
            with open(f"data/{submission.id}.json", "w") as outfile:
                json.dump(json_submission, outfile, indent=4)

def get_parent_body(id):
    time.sleep(random.randint(1, 4))
    comment = reddit.comment(id)
    return comment.body


completed = []


def start_extraction():
    try:
        for subreddit in subreddits_name:
            time.sleep(random.randint(10,20))
            get_comments(subreddit)
            print("Ongoing: ====================>>>>>", subreddit)
            completed.append(subreddit)
    except Exception as e:
        print(e)
        time.sleep(100)
        start_extraction()


start_extraction()