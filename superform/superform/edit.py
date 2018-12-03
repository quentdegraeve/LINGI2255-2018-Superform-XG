from flask import Blueprint, url_for, request, redirect, render_template
from superform.utils import login_required

edit_page = Blueprint('edit', __name__)

@edit_page.route('/edit/<int:post_id>', methods=['GET'])
@login_required()
def edit_post(post_id):
    return render_template('edit.html', post_id=post_id)

@edit_page.route('/edit/publish_edit_post/<int:post_id>', methods=['POST'])
@login_required()
def publish_edit_post(post_id):
    data = request.get_json(force=True)
    print(data)
    return redirect(url_for('index'))
