import coverage
from coverage_diff import main as coverage_diff

MIN_COVERAGE_ALL = 80
MIN_COVERAGE_CHANGES = 80


def run_all_code() -> float:
    cov = coverage.Coverage(config_file='coverage.toml')
    cov.load()
    cov.html_report(directory='./.coverage/all')
    print('COVERAGE OVER ALL')
    return cov.report()


def run_on_changes() -> float:
    cov = coverage.Coverage(config_file='coverage.toml')
    cov.load()
    changed_files = coverage_diff.get_changed_files(
        branch1='HEAD^',
        branch2='HEAD',
        diff_filter='dr',
        include_regexp='\\.py$',
        use_fork_point=False,
    )
    print('COVERAGE ON CHANGED FILES')
    if not changed_files:
        print('- no changes detected')
        return 100
    print('COVERAGE ON CHANGED FILES')
    [print(f) for f in changed_files]
    cov.html_report(include=changed_files, directory='./.coverage/changes')
    return cov.report(include=changed_files)


def run_coverage() -> None:
    coverage_all = run_all_code()
    passed_all = coverage_all >= MIN_COVERAGE_ALL
    coverage_changes = run_on_changes()
    passed_changes = coverage_changes >= MIN_COVERAGE_CHANGES

    if not passed_all:
        print(f'[!] COVERAGE ALL failed {coverage_all}/{MIN_COVERAGE_ALL}')
    if not passed_changes:
        print(f'[!] COVERAGE CHANGES failed {coverage_changes}/{MIN_COVERAGE_CHANGES}')

    if not passed_all or not passed_changes:
        exit(1)


if __name__ == '__main__':
    run_coverage()
