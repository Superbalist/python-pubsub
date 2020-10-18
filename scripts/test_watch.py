#!/usr/bin/env python
import os
import platform

from watchgod import run_process
import pytest
from pytest_jsonreport.plugin import JSONReport


plugin = JSONReport()


def notify(message, title):
    if platform.system() == "Darwin":
        os.system(
            f"osascript -e 'display notification "
            f'"{message}" with title "{title}"\''
        )
    elif platform.system() == "Linux":
        os.system(f'notify-send "{title}" "{message}"')


def run_test():
    pytest.main(plugins=[plugin])
    report = plugin.report

    if report["exitcode"] == 0:
        notify("Test passed", "python-pubsub auto test")
    else:
        notify("Test failed", "python-pubsub auto test")


if __name__ == "__main__":
    run_process(".", run_test)
