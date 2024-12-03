import os.path
import unittest

import coverage
import django
from teamcity import is_running_under_teamcity
from teamcity.unittestpy import TeamcityTestRunner

from config import settings_test


def run():
    print('Initializing unit tests')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings_test'

    print('Running django setup')
    django.setup()

    test_loader = unittest.TestLoader()
    suite = test_loader.suiteClass([])

    for app in settings_test.INSTALLED_APPS:
        test_dir = os.path.join(app.replace('.', os.path.sep), 'tests', 'unit')
        if os.path.exists(test_dir):
            suite.addTest(unittest.TestLoader().discover(test_dir))

    cov = coverage.Coverage(config_file='coverage.toml')
    cov.start()
    cov.switch_context("unit tests")

    if is_running_under_teamcity():
        TeamcityTestRunner().run(suite)
    else:
        unittest.TextTestRunner(verbosity=2).run(suite)

    cov.stop()
    cov.save()


if __name__ == '__main__':
    run()