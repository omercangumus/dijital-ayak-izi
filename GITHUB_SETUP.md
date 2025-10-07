# 🚀 GitHub'a Push Talimatları

## 1. Git Kurulumu

### Windows:
1. https://git-scm.com/download/win adresinden Git'i indirin
2. Kurulum sırasında "Use Git from the command line and also from 3rd-party software" seçin
3. Terminal'i yeniden başlatın

## 2. GitHub Repository Oluşturma

1. GitHub.com'da giriş yapın
2. "New repository" butonuna tıklayın
3. Repository adı: `dijital-ayak-izi` (veya istediğiniz ad)
4. **Private** seçin (önemli!)
5. "Create repository" butonuna tıklayın

## 3. Proje Push Etme

Terminal'de şu komutları çalıştırın:

```bash
# Git repository'sini başlat
git init

# Dosyaları ekle
git add .

# İlk commit
git commit -m "İlk commit: Dijital Ayak İzi Uygulaması"

# GitHub repository'sini remote olarak ekle
git remote add origin https://github.com/KULLANICI_ADINIZ/dijital-ayak-izi.git

# Ana branch'i main olarak ayarla
git branch -M main

# GitHub'a push et
git push -u origin main
```

## 4. Arkadaşları Davet Etme

1. GitHub repository sayfasında "Settings" sekmesine gidin
2. Sol menüden "Manage access" seçin
3. "Invite a collaborator" butonuna tıklayın
4. Arkadaşlarınızın GitHub kullanıcı adını girin
5. "Add" butonuna tıklayın

## 5. Güvenlik Notları

- `config.env` dosyası .gitignore'da olduğu için push edilmeyecek
- API anahtarları güvenli kalacak
- Sadece davet edilen kişiler erişebilecek

## 6. Sonraki Güncellemeler

```bash
# Değişiklikleri ekle
git add .

# Commit et
git commit -m "Güncelleme açıklaması"

# Push et
git push
```

---

**Not**: İlk push'tan sonra arkadaşlarınız `git clone https://github.com/KULLANICI_ADINIZ/dijital-ayak-izi.git` komutu ile projeyi klonlayabilir.
