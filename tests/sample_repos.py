from tempfile import NamedTemporaryFile, mkdtemp
from git import Repo


def get_sample_repos():
    return [
        create_clean_repo(),
        create_dirty_repo(),
    ]


def create_clean_repo():
    directory = mkdtemp(suffix=f"_clean")
    repo = Repo.init(directory)
    return repo


def create_dirty_repo():
    directory = mkdtemp(suffix=f"_dirty")
    file = NamedTemporaryFile(dir=directory, delete=False).name
    repo = Repo.init(directory)
    repo.index.add([file])
    return repo
