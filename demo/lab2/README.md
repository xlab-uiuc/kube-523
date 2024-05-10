# Lab 2

## Collecting the Bug Dataset
Please follow the instructions to collect your bug dataset for study.
This process is important to ensure the study results are representative and unbiased.

### 1. Collect All Closed Issues from the Operator Repository

You need to follow the instructions below depending whether your operator’s issues are hosted on GitHub or JIRA.

**Instruction for GitHub repositories**

The issues can be crawled from the GitHub via its REST API. 
We provide a Python script to automatically crawl the closed issues with the proper filters and dump it into a CSV file.

Usage:
```
python3 crawl_github_issues.py
  --repo REPO           The repository to crawl issues from, e.g., `pravega/zookeeper-operator`
  --github-token GITHUB_TOKEN
                        The GitHub token to use for authentication
```

If you don't know how to generate GitHub authentication tokens, check this [link](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic).

This script will then write a CSV file named with the operator name containing all the closed issues.

**Instruction for JIRA database**

Projects hosted in JIRA databases have slightly different ways for managing bug tickets. The bug reports can be found by going to the “Issues” panel, and applying the following filters:

- Type: Bug
- Status: Done

Then export the issues into a CSV file.

### 2. Shuffle the Rows in the CSV File

You can use the following Python3 code to produce a shuffled CSV file:
```python

df = pd.read_csv(file_name) 
shuffled_df = df.sample(frac=1, random_state=3973120037)
shuffled_df.to_csv(new_file_name, index=False)
```

### 3. Starting from Beginning of the Shuffled CSV, Manually Inspect the Issues to Make Sure They:

- are actually bugs
- are confirmed by the developers
- have clear enough description

### 4. Repeat step 3 until you have 20 issues


## Submitting the Bug Analysis

Please submit the bug analysis for each bug via this [**Google form**](https://forms.gle/FkFkL7H56jQy8QeN7).