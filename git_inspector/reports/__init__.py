from git_inspector.reports.git_report import *
from git_inspector.reports.dirty import get_dirt_repo_report
from git_inspector.reports.merged_branches import get_merged_branches_report
from git_inspector.reports.unpushed import get_unpushed_branches_report
from git_inspector.reports.untracked_branches import get_untracked_branches_report


def get_git_reports(repos):
    all_reports = []
    for repository in repos:
        reports = [
            repository,
            get_dirt_repo_report(repository),
            get_merged_branches_report([repository]),
            get_unpushed_branches_report([repository]),
            get_untracked_branches_report([repository])
        ]
        reports = [r for r in reports if r is not None]
        all_reports.append(reports)
    return all_reports


def get_git_reports_for_repo(repository):
    reports = [
        get_dirt_repo_report(repository),
        get_merged_branches_report([repository]),
        get_unpushed_branches_report([repository]),
        get_untracked_branches_report([repository])
    ]
    reports = [r for r in reports if r is not None]
    return reports