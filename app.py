import praw
import os, shutil, pathlib

reddit = praw.Reddit(
    client_id="s9OQw96pTwsDMmr2_MUUqg",
    client_secret="319sCgCY0EYvKo3UEjFkgsoxVlXeQw",
    user_agent="app by u/UPatel8829",
)

subreddits_name = [
    "interviewpreparations",
    "jobsearchhacks",
    "Resume",
    "jobs",
    "skills"
]


def get_comments(subreddit):
    subreddit = reddit.subreddit(subreddit)
    tops = subreddit.top(limit=2)

    for submission in tops:
        if not submission.stickied:
            score = submission.score
            title = submission.title
            id = submission.id
            id = submission.createdat
            print(f"Title\n{title}\nScore: {score}")

            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                print(40*"=*")
                if comment.body:
                    print("Parent: ",comment.parent())
                    print("Child: ",comment.id)
                    print(comment.body)
                    print(comment.author)
                    print(comment.score)
            #
            # comments = submission.comments.list()
            # for comment in comments:
            #     print(50*"=")
            #     print(comment.body)


get_comments(subreddits_name[0])
