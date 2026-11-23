# Particle Studio

Görselleri küçük parçacıklar veya ASCII karakterler kullanarak aşamalı biçimde oluşturan, paylaşılabilir animasyonlar üreten bir uygulama.

## Temel yaklaşım
- Python: görüntü analizi, parçacık verisi ve animasyon planı.
- Web: kullanıcı arayüzü.
- HTML Export: CSS, JavaScript ve gerekli verileri tek HTML dosyasına gömer. Alıcı tarafında Python kurulumu gerekmez.
- Terminal Export: isteğe bağlı CMD/terminal tabanlı ASCII animasyonu.

## Geliştirme
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -e ".[dev]"
```

## Çalıştırma
İlk uygulama giriş noktası ve arayüz henüz oluşturulma aşamasındadır. İlerleyen aşamada:
```bash
python -m particle_studio
```
