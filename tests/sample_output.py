from git_inspector import inspect_all
from git_inspector.report_formatter import format_git_reports
from tests.sample_repos import get_sample_repos


def get_sample_output():
    repos = get_sample_repos()
    reports = get_sample_reports(repos)
    sample_output = format_git_reports(reports)
    return sample_output


def get_sample_reports(repos):
    reports = inspect_all(paths=[repo.working_tree_dir for repo in repos])
    return reports


if __name__ == '__main__':
    sample_output = get_sample_output()
    print(sample_output)
