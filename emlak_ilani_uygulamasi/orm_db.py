from flask import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import os

YUKLEME_KLASORU = 'static/yuklemeler'
UZANTILAR = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emlak_sistemi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = YUKLEME_KLASORU
app.debug = True
db = SQLAlchemy(app)
dbsession = db.session()

class Yonetici(db.Model):

    yonetici_id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    yonetici_adi_soyadi = db.Column(db.String(50), nullable=False)
    yonetici_tc = db.Column(db.String(11), unique=True, nullable=False)
    yonetici_sifre = db.Column(db.String(10), nullable=False)
    yonetici_email = db.Column(db.String(50))
    yonetici_tel = db.Column(db.String(12))
    yonetici_durum = db.Column(db.Integer, nullable=False)

class Ilan(db.Model):

    ilan_id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    ilan_baslik = db.Column(db.String(50))
    ilan_icerik = db.Column(db.String(500))
    ilan_tarihi = db.Column(db.DateTime, nullable=False, default=datetime.date)

    ilan_semt_id = db.Column(db.Integer, db.ForeignKey('semt.semt_id'), nullable=False)
    semt_id = db.relationship('Semt', backref=db.backref('ilan_semti', lazy=True))

    ilan_evtipi_id = db.Column(db.Integer, db.ForeignKey('evtipi.evtipi_id'), nullable=False)
    evtipi_id = db.relationship('Evtipi', backref=db.backref('ilan_evtipi', lazy=True))
    ilan_turu = db.Column(db.Integer, nullable=False)
    ilan_goruntulenme_sayisi = db.Column(db.Integer, nullable=False,default=0)
    ilan_fiyati = db.Column(db.Integer, nullable=False, default=0)

    ilan_foto_01 = db.Column(db.String(500))
    ilan_foto_02 = db.Column(db.String(500))
    ilan_foto_03 = db.Column(db.String(500))
    ilan_foto_04 = db.Column(db.String(500))
    ilan_foto_05 = db.Column(db.String(500))

    ilan_durum = db.Column(db.Integer, nullable=False)

    ilan_yonetici_id = db.Column(db.Integer, db.ForeignKey('yonetici.yonetici_id'), nullable=False)
    ilan_personel_id = db.Column(db.Integer, db.ForeignKey('yonetici.yonetici_id'), nullable=False)

    yonetici = db.relationship('Yonetici', backref=db.backref('ilan_yonetici', lazy=True),
                               foreign_keys=[ilan_yonetici_id])
    personel = db.relationship('Yonetici', backref=db.backref('ilan_personel', lazy=True),
                               foreign_keys=[ilan_personel_id])


class Semt(db.Model):
    semt_id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    semt_adi = db.Column(db.String(50))

class Evtipi(db.Model):
    evtipi_id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    evtipi_adi = db.Column(db.String(15))



# veri tabanını oluşturmak için tabloyu oluşturmak için
db.create_all()

