# 🚀 GitHub'a Push Talimatları

## ✅ Git Kurulumu Tamamlandı!

Git başarıyla yüklendi ve ilk commit yapıldı. Şimdi GitHub'a push edelim:

## 1. GitHub Repository Oluşturma

1. **GitHub.com**'a gidin ve giriş yapın
2. **"New repository"** butonuna tıklayın (sağ üst köşede + işareti)
3. **Repository adı**: `dijital-ayak-izi` (veya istediğiniz ad)
4. **Açıklama**: "Dijital Ayak İzi Farkındalık Uygulaması"
5. **🔥 ÖNEMLİ: "Private" seçin** (sadece davet edilenler görebilir)
6. **"Create repository"** butonuna tıklayın

## 2. Repository URL'sini Kopyalayın

GitHub'da oluşturduğunuz repository sayfasında **"Code"** butonuna tıklayın ve **HTTPS** URL'sini kopyalayın:
```
https://github.com/KULLANICI_ADINIZ/dijital-ayak-izi.git
```

## 3. Terminal'de Push Komutları

Şu komutları sırayla çalıştırın:

```powershell
# GitHub repository'sini remote olarak ekle
& "C:\Program Files\Git\bin\git.exe" remote add origin https://github.com/KULLANICI_ADINIZ/dijital-ayak-izi.git

# Ana branch'i main olarak ayarla
& "C:\Program Files\Git\bin\git.exe" branch -M main

# GitHub'a push et
& "C:\Program Files\Git\bin\git.exe" push -u origin main
```

## 4. Kimlik Doğrulama

İlk push'ta GitHub kullanıcı adınızı ve şifrenizi (veya Personal Access Token) isteyecek.

### Personal Access Token Oluşturma (Önerilen):
1. GitHub → Settings → Developer settings → Personal access tokens
2. "Generate new token" → "repo" izni verin
3. Token'ı kopyalayın ve şifre olarak kullanın

## 5. Arkadaşları Davet Etme

Repository oluştuktan sonra:
1. Repository sayfasında **"Settings"** sekmesi
2. Sol menüden **"Manage access"**
3. **"Invite a collaborator"** butonuna tıklayın
4. Arkadaşlarınızın GitHub kullanıcı adını girin

## 6. Sonraki Güncellemeler

```powershell
# Değişiklikleri ekle
& "C:\Program Files\Git\bin\git.exe" add .

# Commit et
& "C:\Program Files\Git\bin\git.exe" commit -m "Güncelleme açıklaması"

# Push et
& "C:\Program Files\Git\bin\git.exe" push
```

---

## 🔒 Güvenlik Kontrolü

- ✅ `config.env` dosyası .gitignore'da (API anahtarları korunuyor)
- ✅ Private repository (sadece davet edilenler erişebilir)
- ✅ Hassas dosyalar push edilmiyor

**Hazır! GitHub repository URL'sini aldıktan sonra push komutlarını çalıştırabilirsiniz.** 🎉
