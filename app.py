from flask import Flask, render_template, redirect, url_for
from GoogleDriveTools import GoogleDriveTools
from RenameForm import RenameForm
from secret import secret
from room_ids import rooms_150, rooms_160a, rooms_160b

app = Flask(__name__)
app.config['SECRET_KEY'] = secret

building150Logs = '1ZX9HtwMvPPAmRa_eiy7uHp8HqKWEhCqR'
studioOpsDrive = '0ALGMv4uFp8QxUk9PVA'

driveHelper = GoogleDriveTools(studioOpsDrive)


def process_rooms(room_ids):
    active_rooms = []
    for i in driveHelper.get_active_rooms(room_ids):
        active_rooms.append([i, driveHelper.get_folder_name(i)])
    return active_rooms


@app.route('/')
def main():
    return redirect(url_for('desk_150'))


@app.route('/150', methods=['GET', 'POST'])
def desk_150():
    form = RenameForm()

    if form.validate_on_submit():
        for file in driveHelper.list_files(form.id.data):
            driveHelper.rename_file(file['id'], form.newName.data)
        redirect(url_for('desk_150'))

    active_rooms = process_rooms(rooms_150)

    return render_template('index.html', active_rooms=active_rooms, form=form,
                           active_menu_item='150')


@app.route('/160a', methods=['GET', 'POST'])
def desk_160a():
    form = RenameForm()

    if form.validate_on_submit():
        for file in driveHelper.list_files(form.id.data):
            driveHelper.rename_file(file['id'], form.newName.data)
        redirect(url_for('desk_160a'))

    active_rooms = process_rooms(rooms_160a)

    return render_template('index.html', active_rooms=active_rooms, form=form,
                           active_menu_item='160a')


@app.route('/160b', methods=['GET', 'POST'])
def desk_160b():
    form = RenameForm()

    if form.validate_on_submit():
        for file in driveHelper.list_files(form.id.data):
            driveHelper.rename_file(file['id'], form.newName.data)
        redirect(url_for('desk_160b'))

    active_rooms = process_rooms(rooms_160b)

    return render_template('index.html', active_rooms=active_rooms, form=form,
                           active_menu_item='160b')


if __name__ == '__main__':
    app.run(debug=True)
