from flask import Flask, render_template, redirect, url_for
from GoogleDriveTools import GoogleDriveTools
from RenameForm import RenameForm
from secret import secret

app = Flask(__name__)
app.config['SECRET_KEY'] = secret

building150Logs = '1ZX9HtwMvPPAmRa_eiy7uHp8HqKWEhCqR'
studioOpsDrive = '0ALGMv4uFp8QxUk9PVA'

rooms_150 = ['1JJsj94oT62TjcstJ-KxPPvy-LRNPyOl2',
             '19tzex4MakdkcULh4k1-IPszwE51gt6zH',
             '1we01vHBRnWnz5BxAg5Rth8zmK8dAcInb',
             '1E8IxN7BSZeSTqMMjaBBDMmcFNDuq5GJ8',
             '1sqDANMWOM0_e-6pZtT5cAmKFLq4c2jlD',
             '1mjqq8-KRF1NxFXJcULwPQmUlFkHjxtyj',
             '1dAcz3-7IqvGhNEwx8Fovqiwp4yPX6ixv',
             '1SCnC7ELaiYy6whNLda9ln_Z3ChtoT2Ch',
             '14N9SJ1ONEZ6kOsUo2PZ6vAcihBMKI_Y-',
             '18P44BNiszkqsLoetFO6_rCD2yBaWI1ev',
             '1A7gaQdhgvdo-SyTXwcS5QHIlVNnPKo6b']

rooms_160a = ['1WQ6l85hNfXS5x4QGNruQwhTSSh6dgQ0V',
              '149BjNHII-mVFyc-Dhf_0NNLD1_0NnU62',
              '1s2WXRgM10qa6frIhzz5J3Qn1-_w8RF8k',
              '1j6-rm9V_bdaFFy0Ih_3eC8WD9DzDHo5H',
              '1IE8DusVhidVQ6EvqSHrgfRsOX95nofYU']

rooms_160b = ['1dIcULToyCsDNGT0e_-7aM4yVxBUH9nVr',
              '11lWdWj_Ub0Rk0mpZtvH8YazxMsgzGZer',
              '1KT5q0ZBVYUPvk2CSIXC27pim0pa1Ib94',
              '1KEZi1YUZ7JqU5REgvqNyUOrBKUqv61mY',
              '10YuTj6iuqE2cjQIJUnoxJXnlG0kXIp17',
              '14QARjeKWKRUlCrI0l87_dqHH3xYlnkyu']

driveHelper = GoogleDriveTools(studioOpsDrive)


@app.route('/')
def main():
    return redirect(url_for('desk_150'))


@app.route('/150', methods=['GET', 'POST'])
def desk_150():
    form = RenameForm()

    if form.validate_on_submit():
        for file in driveHelper.list_files(form.id.data):
            driveHelper.rename_file(file['id'], form.newName.data)

    active_rooms = []
    for i in driveHelper.get_active_rooms(rooms_150):
        active_rooms.append([i, driveHelper.get_folder_name(i)])
    return render_template('index.html', active_rooms=active_rooms, form=form,
                           active_menu_item='150')


@app.route('/160a', methods=['GET', 'POST'])
def desk_160a():
    form = RenameForm()

    if form.validate_on_submit():
        for file in driveHelper.list_files(form.id.data):
            driveHelper.rename_file(file['id'], form.newName.data)

    active_rooms = []
    for i in driveHelper.get_active_rooms(rooms_160a):
        active_rooms.append([i, driveHelper.get_folder_name(i)])
    return render_template('index.html', active_rooms=active_rooms, form=form,
                           active_menu_item='160a')


@app.route('/160b', methods=['GET', 'POST'])
def desk_160b():
    form = RenameForm()

    if form.validate_on_submit():
        for file in driveHelper.list_files(form.id.data):
            print(form.newName.data)
            driveHelper.rename_file(file['id'], form.newName.data)

    active_rooms = []
    for i in driveHelper.get_active_rooms(rooms_160b):
        active_rooms.append([i, driveHelper.get_folder_name(i)])
    return render_template('index.html', active_rooms=active_rooms, form=form,
                           active_menu_item='160b')


if __name__ == '__main__':
    app.run(debug=True)
