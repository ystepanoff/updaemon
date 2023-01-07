from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Source, Action


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
    )

@main.route('/source', methods=['GET'])
@login_required
def source_get() -> str:
    source_id = int(request.args.get('id'))
    source = Source.from_id(source_id, current_user.get_id())
    if source is not None:
        return render_template(
            'source.html',
            source_id=source_id,
            source=source,
            actions=Source.list_actions(source_id),
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
    source_id = int(request.form.get('id'))
    source = Source.from_id(source_id, current_user.get_id())
    if source is not None:
        source.name = request.form.get('name')
        source.description = str(request.form.get('description'))
        source.remote = str(request.form.get('remote'))
        source.update(source_id)
    return ''
