# 🛒 Python Fiyat Takip & Alarm Botu

Bu proje, e-ticaret sitelerindeki (Amazon, Trendyol, Hepsiburada vb.) ürünlerin fiyatlarını anlık olarak takip eden, kullanıcı dostu arayüze (GUI) sahip bir masaüstü uygulamasıdır. Belirlediğiniz hedef fiyatın altına düşüldüğünde size **e-posta ile bildirim** gönderir.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 🌟 Özellikler

* **Modern Arayüz:** CustomTkinter ile tasarlanmış "Dark Mode" destekli şık tasarım.
* **Akıllı Seçici:** CSS Class mantığı ile çalışır, bu sayede hemen hemen her sitede kullanılabilir.
* **Anlık Test:** Kaydetmeden önce fiyatın doğru çekilip çekilmediğini test etme imkanı.
* **E-Posta Bildirimi:** Hedef fiyata ulaşıldığında otomatik mail atar.
* **JSON Veritabanı:** Kurulum gerektirmeyen, taşınabilir yerel kayıt sistemi.
* **Detaylı Takip:** Kayıtlı ürünlerin başlangıç fiyatını, hedef fiyatını ve güncel durumunu tablo halinde gösterir.

## 🚀 Kurulum

Projeyi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin.

1.  **Projeyi Klonlayın:**
    ```bash
    git clone [https://github.com/KULLANICI_ADIN/repo-ismin.git](https://github.com/KULLANICI_ADIN/repo-ismin.git)
    cd repo-ismin
    ```

2.  **Gerekli Kütüphaneleri Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Uygulamayı Başlatın:**
    ```bash
    python main.py
    ```

## ⚙️ Ayarlar (Mail Gönderimi İçin)

Uygulama üzerinden mail alabilmek için sağ üstteki **Ayarlar** menüsünden Gmail bilgilerinizi girmeniz gerekir.

> **Önemli:** Güvenlik nedeniyle normal Gmail şifreniz çalışmaz. Google hesabınızdan **"Uygulama Şifresi" (App Password)** oluşturup onu kullanmalısınız.

1.  Google Hesabım > Güvenlik > 2 Adımlı Doğrulama > Uygulama Şifreleri yolunu izleyin.
2.  Yeni bir şifre oluşturun ve uygulamadaki ilgili alana yapıştırın.
3.  Bilgileriniz sadece kendi bilgisayarınızda `ayarlar.json` dosyasında tutulur, sunucuya gönderilmez.

## 📸 Ekran Görüntüleri

*()*

## 🤝 Katkıda Bulunma

1.  Bu projeyi Fork'layın.
2.  Yeni bir özellik dalı (branch) oluşturun (`git checkout -b yeni-ozellik`).
3.  Değişikliklerinizi commit yapın (`git commit -m 'Yeni özellik eklendi'`).
4.  Dalınızı Push yapın (`git push origin yeni-ozellik`).
5.  Bir Pull Request oluşturun.

---
**Geliştirici:** [Ali Fırat Özer]
