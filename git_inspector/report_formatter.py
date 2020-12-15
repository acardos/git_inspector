import itertools
from collections import defaultdict
from git_inspector.config import *
from git_inspector.reports.git_report import GitReport
from git import Head, Repo
from git_inspector.common import is_master_branch
from git_inspector.reports import GIT_REPORT_LEVEL_ALERT, GIT_REPORT_LEVEL_WARNING, GIT_REPORT_LEVEL_HINT


def format_git_reports(git_reports: list):
    lines = []

    for report in git_reports:
        repository = report[0]
        reports = report[1:]
        if all(r.is_empty() for r in reports):
            continue
        lines.append(git_repo_repr(repository))
        report_lines = itertools.chain([
            format_git_report(report)
            for report in reports
        ])

        lines.extend(report_lines)

    sm = summary_string(git_reports)
    lines.append(sm)

    return "\n".join([l for l in lines if l != ""])


def color_s(color, string):
    return f"{color}{string}{COLOR_RESET}"


def format_git_report(git_report: GitReport):
    if git_report.is_empty():
        return ""

    lines = []
    for repository in git_report.repos:
        lines.append(indent_string(color_s(COLORS[git_report.alert_level], git_report.description)))

    for head in git_report.heads:
        lines.append(indent_string(color_s(COLORS[git_report.alert_level], git_report.description)))

    return "\n".join(lines)


def indent_string(string, indent=5):
    return " " * indent + string


def summary_string(git_reports: list):
    a_cnt = count_git_report_alert_level(git_reports)

    if a_cnt[GIT_REPORT_LEVEL_ALERT] == 0 \
            and a_cnt[GIT_REPORT_LEVEL_WARNING] == 0 \
            and a_cnt[GIT_REPORT_LEVEL_HINT] == 0:
        summary = f"{len(git_reports)} git repositories found. Everything looks fine :D"
        summary = COLOR_SUCCESS + summary + COLOR_RESET
        return summary

    summary = f"{SUMMARY_COLOR_NOT_CLEAN}{len(git_reports)} git repositories found {COLOR_RESET}"

    sss = []
    if a_cnt[GIT_REPORT_LEVEL_ALERT] > 0:
        sss.append(f"{COLOR_ALERT}{a_cnt[GIT_REPORT_LEVEL_ALERT]} alerts{COLOR_RESET}")
    if a_cnt[GIT_REPORT_LEVEL_WARNING] > 0:
        sss.append(f"{COLOR_WARNING}{a_cnt[GIT_REPORT_LEVEL_WARNING]} warnings{COLOR_RESET}")
    if a_cnt[GIT_REPORT_LEVEL_HINT] > 0:
        sss.append(f"{COLOR_HINT}{a_cnt[GIT_REPORT_LEVEL_HINT]} hints{COLOR_RESET}")
    if len(sss) == 1:
        summary += f"{SUMMARY_COLOR_NOT_CLEAN}with {sss[0]}{SUMMARY_COLOR_NOT_CLEAN}."
    if len(sss) == 2:
        summary += f"{SUMMARY_COLOR_NOT_CLEAN}with {sss[0]}{SUMMARY_COLOR_NOT_CLEAN} and {sss[1]}{SUMMARY_COLOR_NOT_CLEAN}."
    if len(sss) == 3:
        summary += f"{SUMMARY_COLOR_NOT_CLEAN}with {sss[0]}{SUMMARY_COLOR_NOT_CLEAN}{SUMMARY_COLOR_NOT_CLEAN}, {sss[1]}{SUMMARY_COLOR_NOT_CLEAN} and {sss[2]}{SUMMARY_COLOR_NOT_CLEAN}."

    return summary


def count_git_report_alert_level(git_reports):
    a_cnt = defaultdict(int)
    for repo_report in git_reports:
        repository = repo_report[0]
        reports = repo_report[1:]
        for report in reports:
            a_cnt[report.alert_level] += 1
    return a_cnt


def git_repo_repr(repo: Repo):
    return f"{repo.working_tree_dir}"


def git_head_repr(head: Head):
    return f"{head.repo.working_tree_dir}  {f'{COLOR_BRANCH_TAG}@{head}{COLOR_RESET}' if not is_master_branch(head) else ''}"
