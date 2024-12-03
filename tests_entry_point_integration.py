import os

import coverage
import django
from django.core.management import call_command
from django.test.runner import DiscoverRunner
from teamcity import is_running_under_teamcity
from teamcity.unittestpy import TeamcityTestRunner

os.environ['DJANGO_DEBUG'] = 'false'

from config import settings_test


def run():
    print('Initializing integration tests')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings_test'

    print('Running django setup')
    django.setup()

    test_runner = DiscoverRunner(verbosity=2)
    modules = []
    for app in settings_test.INSTALLED_APPS:
        test_dir = os.path.join(app.replace('.', os.path.sep), 'tests', 'integration')
        if os.path.exists(test_dir):
            modules.append(test_dir)

    cov = coverage.Coverage(config_file='coverage.toml')
    cov.start()
    cov.switch_context("integration tests")

    if is_running_under_teamcity():
        call_command('migrate', verbosity=0)
        test_suite = test_runner.build_suite(modules)
        TeamcityTestRunner().run(test_suite)
    else:
        test_runner.run_tests(modules)

    print(modules)
    cov.stop()
    cov.save()


if __name__ == '__main__':
    run()
