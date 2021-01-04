from orm_db import *
kullanici = {}

# Giriş işlemlerinin yer alacak olduğu işlemler
#giriş karşılama sayfası
@app.route('/', methods=['GET', 'POST'])
@app.route('/')
def index():
        return render_template('index.html')

# Giriş işlemlerinin yer alacak olduğu işlemler
#giriş karşılama sayfası
@app.route('/yonetim', methods=['GET', 'POST'])
@app.route('/yonetim')
def yonetim():
    if request.method == 'POST':
        tc = request.form.get('tcno')
        sifre = request.form.get('sifre')

        if True:

            user = Yonetici.query.filter_by(yonetici_tc=tc, yonetici_sifre=sifre).first()
            if user.yonetici_durum == 0:
                session['yonetici'] = user.yonetici_id
                kullanici['yonetici'] = user
                return redirect(url_for('yonetici_sayfasi'))
            else:
                return render_template('yonetim.html', mesaj="Giriş Yapmak İstediğiniz Kullanıcı Aktif Değil")
        else:
            return render_template('yonetim.html', mesaj="Hatalı giriş Yapmaktasınız")
    else:
        return render_template('yonetim.html', mesaj="Hoş Geldiniz")



#çıkış işlemleri sayfası
@app.route('/cikis')
def cikis():
    session.clear()
    kullanici.clear()

    return redirect(url_for('index'))


#Aşağıdaki ilk bölümde yöneticilerin yapabilecek olduğu iş ve işlemlerin sayfa erişimleri yer almaktadır

#yönetici sayfası işlemleri
@app.route('/yonetici_sayfasi', methods=['GET', 'POST'])
@app.route('/yonetici_sayfasi')
def yonetici_sayfasi():
    try:
        # return redirect(url_for('ilan_listesi'))
        # return render_template('ilan_listesi.html',yonetici=kullanici['yonetici'])
        # dernek_bilgileri = dernek_bilgisi()

        return render_template("yonetici.html",yonetici=kullanici['yonetici'])
    except:
        return render_template('index.html', mesaj="Hoş Geldiniz")


# Personel İşlemleri Aşağıda Bölümde Yer Alacaktır

# personel ekleme işlemleri
@app.route('/personel_ekle', methods=['GET', 'POST'])
@app.route('/personel_ekle')
def personel_ekle():
    try:
        if request.method == 'POST':
            try:
                bilgiler = request.form.to_dict()
                yeni_personel = Yonetici(yonetici_adi_soyadi=bilgiler['yonetici_adi_soyadi'], yonetici_tc=bilgiler['yonetici_tc'],
                                 yonetici_sifre=bilgiler['yonetici_sifre'], yonetici_email=bilgiler['yonetici_email'],
                                 yonetici_tel=bilgiler['yonetici_tel'], yonetici_durum=int(bilgiler['yonetici_durum']),
                                )
                dbsession.add(yeni_personel)
                dbsession.commit()
                return render_template("personel_ekle.html", yonetici=kullanici['yonetici'], mesaj="Başarı")
            except:
                return render_template("personel_ekle.html", yonetici=kullanici['yonetici'] , mesaj="Başarısızlık")
        else:

            return render_template("personel_ekle.html", yonetici=kullanici['yonetici'])
    except:
        return render_template("personel_ekle.html", yonetici=kullanici['yonetici'])

# personel güncelleme ve silme işlemleri
@app.route('/personel_guncelle_sil/<int:id>')
@app.route('/personel_guncelle_sil')
def personel_guncelle_sil(id=0):
    if id == 0:
        personeller = Yonetici.query.all()
        return render_template("personel_guncelle_sil.html", yonetici=kullanici['yonetici'], personeller=personeller)
    else:
        return redirect(url_for('personel_guncelle_sil'))


@app.route('/personel_guncelle/<int:id>')
@app.route('/personel_guncelle', methods=['GET', 'POST'])
def personel_guncelle(id=0):
    if id != 0:
        personel = Yonetici.query.filter_by(yonetici_id=id).first()
        return render_template("personel_guncelle.html", yonetici=kullanici['yonetici'], personel=personel)
    elif request.method == 'POST':
        bilgiler = request.form.to_dict()
        bilgiler['yonetici_durum']=int(bilgiler['yonetici_durum'])
        dbsession.query(Yonetici).filter(Yonetici.yonetici_id==bilgiler['yonetici_id']).update(bilgiler)
        dbsession.commit()
        return redirect(url_for('personel_guncelle_sil'))
    else:
        return redirect(url_for('personel_guncelle'))

#personel silme işlemi yapmak için aşağıdaki kod bloğu
@app.route('/personel_sil/<int:sil>')
def personel_sil(sil=0):
    if sil != 0:
        dbsession.query(Yonetici).filter(Yonetici.yonetici_id == sil).delete()
        dbsession.commit()
        return redirect(url_for('personel_guncelle_sil'))
    else:
        return redirect(url_for('personel_guncelle_sil'))

def uzanti_kontrol(dosyaadi):
   return '.' in dosyaadi and \
   dosyaadi.rsplit('.', 1)[1].lower() in UZANTILAR


# Yönetici ilan İşlemleri

# Yönetici İlan ekleme işlemleri
@app.route('/ilan_ekle', methods=['GET', 'POST'])
@app.route('/ilan_ekle')
def ilan_ekle():
    if request.method == 'POST':
        bilgiler = request.form.to_dict()
        resimler=[]
        resimler.append(request.files['dosya01'])
        resimler.append(request.files['dosya02'])
        resimler.append(request.files['dosya03'])
        resimler.append(request.files['dosya04'])
        resimler.append(request.files['dosya05'])
        i = 1
        for dosya in resimler:
            if dosya and uzanti_kontrol(dosya.filename):
                dosyaadi = secure_filename(dosya.filename)
                dosya.save(os.path.join(app.config['UPLOAD_FOLDER'], dosyaadi))
                dosya_yolu = app.config['UPLOAD_FOLDER'] + "/" + dosyaadi
                deger = "ilan_foto_0"+str(i)
                bilgiler[deger] = dosya_yolu
                i+=1
        if True:
            tarih = datetime.strptime(bilgiler['ilan_tarihi'], '%Y-%m-%d')
            bilgiler['ilan_tarihi'] = datetime.date(tarih)
            yonetici = kullanici['yonetici']
            yeni_ilan = Ilan(ilan_baslik=bilgiler['ilan_baslik'],
                                       ilan_icerik=bilgiler['ilan_icerik'],
                                       ilan_tarihi=bilgiler['ilan_tarihi'],
                                       ilan_semt_id=int(bilgiler['ilan_semt_id']),
                                       ilan_evtipi_id=int(bilgiler['ilan_evtipi_id']),
                                       ilan_turu=int(bilgiler['ilan_turu']),
                                       ilan_fiyati=int(bilgiler['ilan_fiyati']),
                                       ilan_foto_01=bilgiler['ilan_foto_01'],
                                       ilan_foto_02=bilgiler['ilan_foto_02'],
                                       ilan_foto_03=bilgiler['ilan_foto_03'],
                                       ilan_foto_04=bilgiler['ilan_foto_04'],
                                       ilan_foto_05=bilgiler['ilan_foto_05'],
                                       ilan_durum=yonetici.yonetici_durum,
                                       ilan_yonetici_id=yonetici.yonetici_id if yonetici.yonetici_durum == 0 else -1,
                                       ilan_personel_id=yonetici.yonetici_id,
                                       )
            dbsession.add(yeni_ilan)
            dbsession.commit()
            return render_template("ilan_ekle.html", yonetici=kullanici['yonetici'], mesaj="Başarı")
        else:
            return render_template("ilan_ekle.html", yonetici=kullanici['yonetici'], mesaj="Başarısızlık")
    else:
        semtler = Semt.query.all()
        evtipleri = Evtipi.query.all()
        return render_template("ilan_ekle.html", yonetici=kullanici['yonetici'], semtler=semtler, evtipleri=evtipleri)


#
#
 # İlan güncelleme ve silme işlemleri

@app.route('/ilan_guncelle_sil/<int:id>')
@app.route('/ilan_guncelle_sil')
def ilan_guncelle_sil(id=0):
    if id == 0:
        ilanlar = Ilan.query.all()
        return render_template("ilan_guncelle_sil.html", yonetici=kullanici['yonetici'], ilanlar=ilanlar)
    else:
        dbsession.query(Ilan).filter(Ilan.ilan_id== id).delete()
        dbsession.commit()
        return redirect(url_for('ilan_guncelle_sil'))
#

@app.route('/ilan_guncelle/<int:id>')
@app.route('/ilan_guncelle', methods=['GET', 'POST'])
def ilan_guncelle(id=0):
    if id != 0:
        kategoriler = Suckategorisi.query.all()
        hukumlu = Hukumlu.query.filter_by(hukumlu_id=id).first()
        koguslar = Kogus.query.all()
        hukumlu.hukumlu_suc_kategorileri = eval(hukumlu.hukumlu_suc_kategorileri)
        return render_template("hukumlu_guncelle.html", yonetici=kullanici['yonetici'],
                               koguslar=koguslar, hukumlu=hukumlu,kategoriler=kategoriler)
    elif request.method == 'POST':
        bilgiler = request.form.to_dict()
        dosya = request.files['dosya']
        multiselect = request.form.getlist('hukumlu_suc_kategorileri')
        bilgiler['hukumlu_suc_kategorileri'] = str(multiselect)
        tarih = datetime.strptime(bilgiler['hukumlu_baslangic_tarihi'], '%Y-%m-%d')
        bilgiler['hukumlu_baslangic_tarihi'] = datetime.date(tarih)
        tarih = datetime.strptime(bilgiler['hukumlu_bitis_tarihi'], '%Y-%m-%d')
        bilgiler['hukumlu_bitis_tarihi'] = datetime.date(tarih)
        if dosya and uzanti_kontrol(dosya.filename):
            dosyaadi = secure_filename(dosya.filename)
            dosya.save(os.path.join(app.config['UPLOAD_FOLDER'], dosyaadi))
            dosya_yolu = app.config['UPLOAD_FOLDER'] + "/" + dosyaadi
            bilgiler['hukumlu_resmi'] = dosya_yolu

        dbsession.query(Hukumlu).filter(Hukumlu.hukumlu_id==bilgiler['hukumlu_id']).update(bilgiler)
        dbsession.commit()
        return redirect(url_for('hukumlu_guncelle_sil'))

    else:
        return redirect(url_for('hukumlu_guncelle_sil'))







if __name__ == '__main__':
    app.run(debug=True)
