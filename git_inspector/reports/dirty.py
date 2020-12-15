from git import Repo
from git_inspector.reports.git_report import GitReport, GIT_REPORT_LEVEL_ALERT


def get_dirt_repo_report(repo: Repo):
    if not repo.is_dirty():
        return None

    return GitReport(
        'dirty',
        'repository is dirty',
        GIT_REPORT_LEVEL_ALERT,
        [repo],
        [])
