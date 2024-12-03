import click
import json
import os
import shutil
import tempfile
import uuid
from cookiecutter.main import cookiecutter
from django.core.management.base import BaseCommand
from git import Repo
from git import exc


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-t', '--cookiecutter_template',
            type=str,
            default='git+ssh://git@github.com/Eutima/eutima-django-cookiecutter',
            help='the cookiecutter you want to use'
        )

    def handle(self, *args, **options):
        self.git_check()
        cookiecutter_copy, migrations_copy= self.backup()

        cookiecutter_template = options['cookiecutter_template']
        try:
            with open(cookiecutter_copy) as f:
                data = json.load(f)

            shutil.rmtree('apps/core')
            cookiecutter(
                cookiecutter_template,
                extra_context=data,
                overwrite_if_exists=True,
                no_input=True,
                output_dir='..'
            )
            click.echo(click.style('''
[ଳ] Don't forget to apply the migrations
python manage.py makemigrations
python manage.py migrate
            ''', fg='yellow'))
        finally:
            self.restore_backup(cookiecutter_copy, migrations_copy)

    def git_check(self):
        try:
            repo = Repo('.')
            has_uncommitted_changes = repo.is_dirty() or len(repo.untracked_files) > 0
            if has_uncommitted_changes:
                click.echo(click.style(
                    '[ଳ] before running the cookiecutter you need to commit the changes',
                    fg='red'
                ))
                exit(0)
        except exc.InvalidGitRepositoryError:
            click.echo(click.style(
                '[ଳ] before running the cookiecutter you need to initialize a git repo and commit the changes',
                fg='red'
            ))
            exit(0)

    def backup(self):
        migrations_copy = os.path.join(
            tempfile.gettempdir(),
            f'migrations-{uuid.uuid4().hex}'
        )
        cookiecutter_copy = os.path.join(
            tempfile.gettempdir(),
            f'cookiecutter-{uuid.uuid4().hex}.json'
        )
        shutil.move('cookiecutter.json', cookiecutter_copy)
        shutil.move('apps/core/migrations', migrations_copy)
        return cookiecutter_copy, migrations_copy

    def restore_backup(self, cookiecutter_copy, migrations_copy):
        shutil.move(cookiecutter_copy, 'cookiecutter.json')
        shutil.rmtree('apps/core/migrations')
        shutil.move(migrations_copy, 'apps/core/migrations')
