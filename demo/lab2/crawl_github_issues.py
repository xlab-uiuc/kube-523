import argparse
import csv

from github import Github

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo",
        type=str,
        required=True,
        help="The repository to crawl issues from, e.g., `pravega/zookeeper-operator`",
    )
    parser.add_argument(
        "--github-token",
        type=str,
        required=True,
        help="The GitHub token to use for authentication",
    )
    args = parser.parse_args()

    output = args.repo.replace("/", "_") + ".csv"
    g = Github(args.github_token)
    repo = g.get_repo(args.repo)

    with open(output, mode="w") as f:
        csv_writer = csv.writer(
            f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        csv_writer.writerow(["URL", "Title", "Issue Number"])
        issues = repo.get_issues(state="closed")

        for issue in issues:
            if issue.pull_request is None:
                csv_writer.writerow([issue.html_url, issue.title, issue.number])
