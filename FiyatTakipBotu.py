import customtkinter as ctk
import requests
from bs4 import BeautifulSoup
from tkinter import messagebox
import json
import os
import webbrowser

# Tema Ayarları
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Dosya İsimleri
JSON_FILE = "takip_listesi.json"
CONFIG_FILE = "ayarlar.json"

class FiyatTakipApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Ana Pencere Ayarları ---
        self.title("Fiyat Takip Botu Pro v5")
        self.geometry("750x650")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)

        # Başlık ve Ayarlar
        self.frame_top = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_top.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        self.label_title = ctk.CTkLabel(self.frame_top, text="Fiyat Takip Sistemi", font=("Roboto Medium", 24))
        self.label_title.pack(side="left")

        self.btn_settings = ctk.CTkButton(self.frame_top, text="⚙ Ayarlar", width=80, command=self.pencere_ayarlar)
        self.btn_settings.pack(side="right")

        # --- Veri Giriş Alanı (GÜNCELLENDİ) ---
        self.frame_inputs = ctk.CTkFrame(self)
        self.frame_inputs.grid(row=1, column=0, padx=20, pady=10)

        # 1. Satır: URL (Geniş)
        self.entry_url = ctk.CTkEntry(self.frame_inputs, placeholder_text="Ürün Linkini Buraya Yapıştırın", width=620)
        self.entry_url.grid(row=0, column=0, columnspan=4, padx=10, pady=(15, 10))

        # 2. Satır: Selector | ? | Hedef Fiyat
        # Class Selector
        self.combo_selector = ctk.CTkComboBox(self.frame_inputs, values=["prc-dsc", "a-price-whole", "product-price", "price"], width=280)
        self.combo_selector.set("prc-dsc")
        self.combo_selector.grid(row=1, column=0, padx=(10, 5), pady=10)

        # Soru İşareti Butonu (?)
        self.btn_help = ctk.CTkButton(self.frame_inputs, text="?", width=30, fg_color="#7f8c8d", hover_color="#95a5a6", command=self.bilgi_notu_goster)
        self.btn_help.grid(row=1, column=1, padx=(0, 10), pady=10)

        # Hedef Fiyat
        self.entry_target = ctk.CTkEntry(self.frame_inputs, placeholder_text="Hedef Fiyat (TL)", width=280)
        self.entry_target.grid(row=1, column=2, padx=10, pady=10)

        # 3. Satır: Butonlar (Test Et | Kaydet)
        self.btn_test = ctk.CTkButton(self.frame_inputs, text="Anlık Fiyat Görüntüle (Test)", command=self.anlik_test_et, fg_color="#34495e", width=280)
        self.btn_test.grid(row=2, column=0, columnspan=2, padx=10, pady=15)

        self.btn_add = ctk.CTkButton(self.frame_inputs, text="+ Listeye Ekle ve Takibe Başla", command=self.takibe_al, fg_color="#2ecc71", width=280)
        self.btn_add.grid(row=2, column=2, padx=10, pady=15)

        # --- Aksiyon Butonları ---
        self.btn_view = ctk.CTkButton(self, text="📋 Kayıtlı Ürünleri ve Fiyatları Gör", command=self.pencere_kayitlar, height=50, font=("Roboto", 16))
        self.btn_view.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

        # Log Ekranı
        self.textbox_log = ctk.CTkTextbox(self, width=700, height=200)
        self.textbox_log.grid(row=3, column=0, padx=20, pady=10)
        self.log_yaz("Sistem hazır. Class ismini bilmiyorsanız '?' butonuna tıklayın.")

    # --- YENİ EKLENEN FONKSİYONLAR ---
    def bilgi_notu_goster(self):
        """Özel tasarım bilgi penceresi"""
        info_win = ctk.CTkToplevel(self)
        info_win.title("Class Nedir?")
        info_win.geometry("400x250")
        info_win.attributes("-topmost", True) # En üstte tut

        ctk.CTkLabel(info_win, text="Web Sitesi Yapıları Hakkında", font=("Roboto Medium", 16), text_color="#3498db").pack(pady=15)

        aciklama = (
            "Amazon, Trendyol, N11 gibi siteler fiyat bilgilerini\n"
            "HTML kodlarında farklı 'Class' isimleri içinde tutar.\n\n"
            "Örn: Trendyol -> 'price'\n"
            "Örn: Amazon -> 'a-price-whole'\n\n"
            "Doğru class'ı bulup bulmadığınızı anlamak için\n"
            "önce 'Anlık Fiyat Görüntüle' butonunu kullanın."
        )
        ctk.CTkLabel(info_win, text=aciklama, justify="left").pack(pady=10)
        ctk.CTkButton(info_win, text="Anladım", command=info_win.destroy, width=100).pack(pady=10)

    def anlik_test_et(self):
        """Kaydetmeden önce fiyatı test etmek için"""
        url = self.entry_url.get()
        selector = self.combo_selector.get()

        if not url:
            self.log_yaz("HATA: Lütfen önce bir link girin.")
            return

        self.log_yaz("Test ediliyor, siteye bağlanılıyor...")
        self.update()
        
        fiyat = self.web_scrape(url, selector)
        
        if fiyat:
            self.log_yaz(f"BAŞARILI! Çekilen Fiyat: {fiyat} TL")
            # Kullanıcıya görsel olarak da gösterelim
            messagebox.showinfo("Sonuç", f"Fiyat Başarıyla Çekildi!\n\nFiyat: {fiyat} TL")
        else:
            self.log_yaz("BAŞARISIZ! Fiyat çekilemedi. Class ismini kontrol edin.")
            messagebox.showerror("Hata", "Fiyat bulunamadı!\nClass ismini veya Linki kontrol edin.")

    # --- ESKİ YARDIMCI FONKSİYONLAR ---
    def log_yaz(self, mesaj):
        self.textbox_log.insert("0.0", f"> {mesaj}\n")

    def fiyat_temizle(self, fiyat_str):
        temiz = fiyat_str.replace("TL", "").replace("tl", "").strip()
        temiz = temiz.replace(".", "").replace(",", ".")
        try:
            return float(temiz)
        except ValueError:
            return None

    def web_scrape(self, url, selector):
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                tag = soup.find(class_=selector)
                if tag:
                    return self.fiyat_temizle(tag.text)
        except Exception as e:
            print(e)
        return None

    # --- DİĞER PENCERELER (AYARLAR & KAYITLAR) ---
    def pencere_ayarlar(self):
        toplevel = ctk.CTkToplevel(self)
        toplevel.title("Mail Ayarları")
        toplevel.geometry("400x300")
        toplevel.attributes("-topmost", True)

        ctk.CTkLabel(toplevel, text="Gmail Bilgileri", font=("Roboto Medium", 16)).pack(pady=20)
        entry_mail = ctk.CTkEntry(toplevel, placeholder_text="Gmail Adresiniz", width=300)
        entry_mail.pack(pady=10)
        entry_pass = ctk.CTkEntry(toplevel, placeholder_text="Uygulama Şifresi (App Password)", show="*", width=300)
        entry_pass.pack(pady=10)

        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                conf = json.load(f)
                entry_mail.insert(0, conf.get("mail", ""))
                entry_pass.insert(0, conf.get("password", ""))

        def kaydet():
            data = {"mail": entry_mail.get(), "password": entry_pass.get()}
            with open(CONFIG_FILE, "w") as f:
                json.dump(data, f)
            messagebox.showinfo("Başarılı", "Ayarlar kaydedildi!", parent=toplevel)
            toplevel.destroy()
        ctk.CTkButton(toplevel, text="Kaydet", command=kaydet).pack(pady=20)

    def pencere_kayitlar(self):
        if not os.path.exists(JSON_FILE):
            messagebox.showwarning("Boş", "Henüz kayıtlı ürün yok.")
            return
        
        rec_window = ctk.CTkToplevel(self)
        rec_window.title("Takip Listesi")
        rec_window.geometry("900x500")
        rec_window.attributes("-topmost", True)

        headers = ["Ürün Linki", "Başlangıç", "HEDEF", "ŞU ANKİ", "Durum"]
        header_frame = ctk.CTkFrame(rec_window)
        header_frame.pack(fill="x", padx=10, pady=5)
        for h in headers:
            ctk.CTkLabel(header_frame, text=h, font=("Roboto", 12, "bold"), width=150).pack(side="left", padx=5)

        scroll_frame = ctk.CTkScrollableFrame(rec_window, width=880, height=400)
        scroll_frame.pack(padx=10, pady=10)

        with open(JSON_FILE, "r", encoding="utf-8") as f:
            urunler = json.load(f)

        for urun in urunler:
            row_frame = ctk.CTkFrame(scroll_frame)
            row_frame.pack(fill="x", pady=2)
            
            # Bu pencere açılırken hız kazandırmak için fiyat çekmeyi opsiyonel yapabiliriz
            # Ama şimdilik anlık çekiyoruz
            guncel_fiyat = self.web_scrape(urun["url"], urun["selector"])
            baslangic = urun.get("baslangic_fiyat", 0)
            hedef = urun["hedef_fiyat"]

            renk = "#2ecc71" if (guncel_fiyat and guncel_fiyat <= hedef) else ("#e74c3c" if guncel_fiyat else "gray")
            
            ctk.CTkButton(row_frame, text="Siteye Git", width=150, fg_color="#34495e", command=lambda u=urun["url"]: webbrowser.open(u)).pack(side="left", padx=5)
            ctk.CTkLabel(row_frame, text=f"{baslangic} TL", width=150).pack(side="left", padx=5)
            ctk.CTkLabel(row_frame, text=f"{hedef} TL", width=150, text_color="orange").pack(side="left", padx=5)
            ctk.CTkLabel(row_frame, text=f"{guncel_fiyat or '?'} TL", width=150, text_color=renk, font=("Roboto", 14, "bold")).pack(side="left", padx=5)
            ctk.CTkLabel(row_frame, text="DÜŞTÜ!" if renk == "#2ecc71" else "Beklemede", width=150).pack(side="left", padx=5)
            rec_window.update()

    def takibe_al(self):
        url = self.entry_url.get()
        selector = self.combo_selector.get()
        target = self.entry_target.get()

        if not (url and target):
            messagebox.showwarning("Eksik", "URL ve Hedef Fiyat zorunludur!")
            return

        self.log_yaz("Başlangıç fiyatı kontrol ediliyor...")
        self.update()
        suanki_fiyat = self.web_scrape(url, selector) or 0

        yeni_kayit = {"url": url, "selector": selector, "hedef_fiyat": float(target), "baslangic_fiyat": suanki_fiyat}

        data = []
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                try: data = json.load(f)
                except: pass
        
        data.append(yeni_kayit)
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        self.log_yaz(f"Kaydedildi! Başlangıç: {suanki_fiyat} TL")
        self.entry_url.delete(0, 'end')

if __name__ == "__main__":
    app = FiyatTakipApp()
    app.mainloop()