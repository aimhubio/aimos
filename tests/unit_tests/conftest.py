import os
import shutil

from aimos.sdk.repo import Repo, _get_tracking_queue
from aimcore.web.utils import exec_cmd
from aimcore.cli.ui import build_db_upgrade_command
from aimos.sdk.configs import AIM_REPO_NAME, AIM_ENV_MODE_KEY
from aimos.core.utils.tracking import analytics

TEST_REPO_PATH = '.aim-test-repo'


def _init_test_repo():
    Repo.default_repo(init=True)


def _cleanup_test_repo(path):
    shutil.rmtree(TEST_REPO_PATH)


def _upgrade_api_db():
    db_cmd = build_db_upgrade_command()
    exec_cmd(db_cmd, stream_output=True)


def pytest_sessionstart(session):
    analytics.dev_mode = True

    os.environ[AIM_REPO_NAME] = TEST_REPO_PATH
    os.environ[AIM_ENV_MODE_KEY] = 'test'

    _init_test_repo()
    _upgrade_api_db()


def pytest_sessionfinish(session, exitstatus):
    _cleanup_test_repo(TEST_REPO_PATH)
    del os.environ[AIM_REPO_NAME]
