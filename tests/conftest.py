import subprocess
import os
import psutil
import pytest
import signal
from lib.my_requests import Book

APP_PATH = 'C:\\PycharmProjects\\test_for_bi.zone\\test-app\\test-app-win64.exe'


@pytest.fixture(scope='session', autouse=True)
def setup_fixture(request):
    subprocess.Popen(APP_PATH, stdout=False)
    Book.create_session_before_start_testing()
    yield
    kill_process()


@pytest.fixture
def clean_db():
    kill_process()
    subprocess.Popen(APP_PATH)


def kill_process(path: str = APP_PATH):
    name = os.path.basename(path)
    for pid in (process.pid for process in psutil.process_iter() if process.name() == name):
        os.kill(pid, signal.SIGINT)
