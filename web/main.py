import json
from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user

from .models import Source, Scraper, Action, SourceAction


main = Blueprint('main', __name__)


@main.route('/')
def index() -> str:
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile() -> str:
    return render_template(
        'profile.html',
        name=current_user.name,
        sources=current_user.list_sources(),
        base_scrapers=Scraper.list_base_scrapers(),
    )


@main.route('/source', methods=['GET'])
@login_required
def source_get() -> str:
    source_id = int(request.args.get('id'))
    user_id = int(current_user.get_id())
    source = Source.from_id(source_id, user_id)
    if source is not None:
        return render_template(
            'source.html',
            source_id=source_id,
            source=source,
            base_scrapers=Scraper.list_base_scrapers(),
            actions=Source.list_actions(source_id, user_id),
            base_actions=Action.list_base_actions(),
        )
    flash('Source not found.')
    return render_template(
        'profile.html',
        name=current_user.name,
        sources=current_user.list_sources(),
    )


@main.route('/source', methods=['POST'])
@login_required
def source_post() -> str:
    source_id = request.form.get('source_id')
    if source_id is not None:
        source_id = int(source_id)
        source = Source.from_id(source_id, current_user.get_id())
        if source is not None:
            delete = request.form.get('delete', False)
            if delete:
                source.delete(source_id)
            else:
                source.name = request.form.get('name')
                source.description = str(request.form.get('description'))
                source.remote = str(request.form.get('remote'))
                source.scraper_id = int(request.form.get('scraper_id'))
                source.params = json.loads(request.form.get('params', '{}'))
                source.update(source_id)
    else:
        name = request.form.get('name')
        description = request.form.get('description')
        remote = request.form.get('remote')
        scraper_id = request.form.get('scraper_id')
        params = json.loads(request.form.get('params'))
        source = Source(current_user.get_id(), name, description, remote, scraper_id, params)
        source.save()
    return ''



@main.route('/action', methods=['POST'])
@login_required
def action_post() -> str:
    source_id = int(request.form.get('source_id'))
    source = Source.from_id(source_id, current_user.get_id())
    if source is not None:
        source_action_id = request.form.get('source_action_id')
        if source_action_id is None:
            params = json.loads(request.form.get('params'))
            action_id = int(request.form.get('action_id'))
            source_action = SourceAction(source_id, action_id, params)
            source_action.save()
        else:
            source_action_id = int(source_action_id)
            source_action = SourceAction.from_id(source_action_id, current_user.get_id())
            delete = request.form.get('delete', False)
            if delete:
                source_action.delete(source_action_id)
            else:
                source_action.action_id = action_id
                source_action.params = params
                source_action.update(source_action_id)
    return ''
