from flask import Flask, render_template, request, jsonify
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

driveHelper = GoogleDriveTools(studioOpsDrive)


@app.route('/', methods=['GET', 'POST'])
def main():
    form = RenameForm()

    if form.validate_on_submit():
        for file in driveHelper.list_files(form.id.data):
            driveHelper.rename_file(file['id'], form.newName.data)

    active_rooms = []
    for i in driveHelper.get_active_rooms(rooms_150):
        active_rooms.append([i,driveHelper.get_folder_name(i)])
    return render_template('index.html', active_rooms=active_rooms, form=form)


if __name__ == '__main__':
    app.run(debug=True)
