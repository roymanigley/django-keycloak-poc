import enum
import json
import os
import re
import copy
import click
from django.core.management.base import BaseCommand


class ModelActions(enum.Enum):
    ADD_MODEL = 'Add a model'
    EDIT_MODEL = 'Edit a model'
    DELETE_MODEL = 'Delete a model'


class ModelFieldAction(enum.Enum):
    ADD_FIELD = 'Add a field'
    CHANGE_FIELD = 'Change a field'
    REMOVE_FIELD = 'Remove a field'


class FieldType(enum.Enum):
    RELATIONSHIP = 'Relationship'
    CHOICES_FIELD = 'ChoicesField'
    CHAR_FIELD = 'CharField'
    TEXT_FIELD = 'TextField'
    DATE_FIELD = 'DateField'
    TIME_FIELD = 'TimeField'
    DATE_TIME_FIELD = 'DateTimeField'
    BOOLEAN_FIELD = 'BooleanField'
    JSON_FIELD = 'JSONField'
    FILE_FIELD = 'FileField'


def get_field_attributes(field_type: FieldType) -> dict:
    default_values = {
        'required': {'type': bool}
    }
    if field_type == FieldType.RELATIONSHIP.value:
        default_values['cascade'] = {'type': bool}
        default_values['relation'] = {'type': 'select'}
    if field_type == FieldType.CHOICES_FIELD.value:
        default_values['choices'] = {'type': list}
    if field_type == FieldType.CHAR_FIELD.value:
        default_values['max_length'] = {'type': int}
    if field_type == FieldType.FILE_FIELD.value:
        default_values['upload_to'] = {'type': str}

    return default_values


def select_by_index(message, choices):
    while True:
        click.echo(message)
        for i, choice in enumerate(choices, start=1):
            click.echo(click.style(f'  {i}', fg='yellow') + f': {choice}')
        selected_index = click.prompt(click.style('Enter the number:', fg='yellow'), type=int, prompt_suffix='')
        if 1 <= selected_index <= len(choices):
            return choices[selected_index - 1]
        click.echo(click.style(f'[ଳ] {selected_index} is not valid', fg='red'))


def select_boolean(message):
    return click.confirm(click.style(f'{message} [Y/n]:', fg='yellow'), default=True, prompt_suffix='',
                         show_default=False)


def select_int(message):
    return click.prompt(click.style(f'{message}:', fg='yellow'), type=int, prompt_suffix='')


def select_text(message):
    return click.prompt(click.style(f'{message}:', fg='yellow'), type=str, prompt_suffix='')


def select_list(message):
    click.echo('[ଳ] enter the values comma separated')
    text = click.prompt(click.style(f'{message}:', fg='yellow'), type=str, prompt_suffix='')
    return re.split(',\\s*', text)


def prompt_inputs():
    data_file = 'cookiecutter.json'
    if os.path.exists(data_file):
        with open(data_file) as f:
            data = json.load(f)
    else:
        data = {'_models': {}}

    model_field_action, model_name = handle_model_action(data)
    handle_field_action(data, model_field_action, model_name)

    json_data = json.dumps(data, indent=2)
    click.echo(click.style(json_data, fg='green'))
    save_changes = select_boolean('do you want to save the changes?')

    if save_changes:
        with open(data_file, 'w') as f:
            f.write(json_data)

    click.echo(click.style('[ଳ] to update the project run the following command:\npython management.py cookiecutter_run', fg='green'))


def handle_field_action(data, model_field_action, model_name):
    field_name = None

    if model_field_action == ModelFieldAction.REMOVE_FIELD.value:
        field_name = select_by_index('select a field', list(data['_models'][model_name]['fields'].keys()))
        data['_models'][model_name]['fields'].pop(field_name)

    elif model_field_action == ModelFieldAction.ADD_FIELD.value:
        field_name = select_text('new field name')
    elif model_field_action == ModelFieldAction.CHANGE_FIELD.value:
        field_name = select_by_index('select a field', list(data['_models'][model_name]['fields'].keys()))
        data['_models'][model_name]['fields'].pop(field_name)
        field_name = select_text('new field name')

    if model_field_action in [ModelFieldAction.ADD_FIELD.value, ModelFieldAction.CHANGE_FIELD.value]:
        data['_models'][model_name]['fields'][field_name] = {}
        field_type = select_by_index('select a type', [t.value for t in FieldType])
        data['_models'][model_name]['fields'][field_name]['type'] = field_type
        field_attributes = get_field_attributes(data['_models'][model_name]['fields'][field_name]['type'])
        field = data['_models'][model_name]['fields'][field_name]
        field['attributes'] = {}
        for key, value in field_attributes.items():
            selection = None
            if value['type'] == bool:
                selection = select_boolean(key)
            elif value['type'] == str:
                selection = select_text(key)
            elif value['type'] == int:
                selection = select_int(key)
            elif value['type'] == list:
                selection = select_list(key)
            elif value['type'] == 'select':
                selection = select_by_index(key, list(data['_models'].keys()))
            else:
                click.echo(click.style(
                    f'there is no selection option for this type {value["type"]}\nthe value for {key} will be set to None',
                    fg='red'))
            field['attributes'][key] = selection


def handle_model_action(data):
    model_action = select_by_index('what do you want to do?', [a.value for a in ModelActions])
    model_field_action = None
    if model_action == ModelActions.ADD_MODEL.value:
        model_name = select_text('model name')
        data['_models'][model_name] = {'fields': {}}
        model_field_action = ModelFieldAction.ADD_FIELD.value
    else:
        model_name = select_by_index('select a model', list(data['_models'].keys()))
    if model_action == ModelActions.DELETE_MODEL.value:
        data['_models'].pop(model_name)
        for _model_name, model in copy.deepcopy(data['_models']).items():
            for field_name, field in model['fields'].items():
                if field['type'] == FieldType.RELATIONSHIP.value and field['attributes']['relation'] == model_name:
                    data['_models'][_model_name]['fields'].pop(field_name)


    if model_action == ModelActions.EDIT_MODEL.value:
        model_field_action = select_by_index('what do you want to do?', [a.value for a in ModelFieldAction])
    return model_field_action, model_name


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            prompt_inputs()
        except click.exceptions.Abort:
            click.echo(click.style('\n\n[ଳ] RAGE QUIT!', fg='magenta'))
