from app.model.user import Users
from app import response, app
from flask import request, redirect, url_for
from app import db

def index():
    try:
        users = Users.query.all()
        data = transform(users)
        return response.ok(data, "")
    except Exception as e:
        print(e)

def transform(users):
    aray = []
    for i in users:
        aray.append({
            'id' : i.id,
            'name' : i.name,
            'email' : i.email
        })
    return aray
    
def show(id):
    try:
        users = Users.query.filter_by(id=id).first()
        if not users:
            return response.badRequest([], 'Pengguna tidak ditemukan')

        data = singleTransform(users)
        return response.ok(data, "")

    except Exception as e:
        print(e)

        
def singleTransform(users):
    data = {
        'id' : users.id,
        'name' : users.name,
        'email' : users.email
    }
    return data



def store():
    try:
        name = request.form['inpNama']
        email = request.form['inpEmail']
        password = request.form['inpPass']

        # Cek apakah email sudah digunakan
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            return response.badRequest([], 'Email sudah digunakan. Silakan gunakan email lain.')

        # Buat objek user baru
        new_user = Users(name=name, email=email)
        new_user.setPassword(password)

        # Simpan user baru ke database
        db.session.add(new_user)
        db.session.commit()

        data = singleTransform(new_user)
        print(data)
        return response.ok(data, 'Pendaftaran berhasil!')

    except Exception as e:
        print(e)
        return response.badRequest([], 'Terjadi kesalahan. Silakan coba lagi nanti.')
        
def update(id):
    try:
        user = Users.query.filter_by(id=id).first()
        if not user:
            return response.badRequest([], 'Pengguna tidak ditemukan')

        # Ambil data yang dikirimkan dalam permintaan
        data = request.json
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.setPassword(data['password'])

        db.session.commit()

        return response.ok('', 'Berhasil memperbarui data!')

    except Exception as e:
        print(e)

        
def delete(id):
    try:
        user = Users.query.filter_by(id=id).first()
        if not user:
            return response.badRequest([], 'Pengguna tidak ditemukan')

        db.session.delete(user)
        db.session.commit()

        return response.ok('', 'Berhasil menghapus data!')

    except Exception as e:
        print(e)
        
def login():
    try:
        email = request.form['inpEmail']
        password = request.form['inpPass']

        user = Users.query.filter_by(email=email).first()
        if not user:
            return response.badRequest([], 'Email Salah')

        if not user.checkPassword(password):
            return response.badRequest([], 'Login gagal. Cek kembali password anda')
        
        # Jika email dan password benar, berikan respons JSON
        data = singleTransform(user)
        return response.ok(data, "Login berhasil")

    except Exception as e:
        print(e)
        return response.badRequest([], 'Terjadi kesalahan. Silakan coba lagi nanti.')



