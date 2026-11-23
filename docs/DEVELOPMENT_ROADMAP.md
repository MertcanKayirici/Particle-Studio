# Particle Studio --- Geliştirme Yol Haritası

## 1. Amaç

Bu yol haritası, Particle Studio'nun fikir aşamasından çalışan ve
paylaşılabilir çıktılar üreten ilk sürümüne kadar izlenecek geliştirme
sırasını tanımlar. Aşamalar bağımlılıklara göre sıralanmıştır; sonraki
aşamaya geçmeden önce mevcut aşamanın temel kabul kriterleri
karşılanmalıdır.

## 2. Sabit ürün kararları

-   İşleme ve parçacık motoru: Python.
-   Kullanıcı arayüzü: Web tabanlı.
-   Görsel yapıtaşı: Tek parçacık (`Particle`).
-   Girdi: Renkli veya siyah-beyaz görüntü.
-   Çıktı renk modu: Siyah-beyaz veya renkli.
-   Arka plan: Varsayılan olarak siyah.
-   Ana animasyon: Boş/koyu ekrandan başlayıp görüntünün parçacıklarla
    aşamalı oluşması.
-   Birincil çıktı: Tek dosyalık, mobil uyumlu HTML.
-   İkincil çıktı: Tek dosyalık terminal çıktısı; ilk hedef Windows
    `.cmd`.

## 3. Aşamalar

### Phase 0 --- Proje temeli ve sözleşmeler

**Hedef:** Kodlamadan önce modül sınırlarını ve ortak veri
sözleşmelerini belirlemek.

İşler: - Proje klasör yapısını oluşturmak. - Mimari ve algoritma
dokümanlarını referans kabul etmek. - Veri modellerini tanımlamak. -
Görüntü örnekleme, parçacık ve animasyon kurallarını yazılı hale
getirmek. - Python sürümü ve temel bağımlılıkları belirlemek.

Çıkış kriteri: - Modüllerin sorumlulukları ve birbirleriyle veri
alışverişi açık olmalı.

### Phase 1 --- Image Processing Core

**Hedef:** Girdi görüntüsünü parçacık üretimine uygun, normalize edilmiş
veriye dönüştürmek.

İşler: - Görüntü yükleme ve doğrulama. - RGB/RGBA ve grayscale
desteği. - Boyutlandırma ve en-boy oranını koruma. - Parlaklık, kontrast
ve gamma işlemleri. - Gürültü/iyileştirme adımlarını kontrollü
uygulama. - Örnekleme için yoğunluk haritası hazırlama.

Çıkış kriteri: - Farklı boyut ve renk modlarındaki görüntüler tutarlı
biçimde işlenebilmeli.

### Phase 2 --- Particle Engine

**Hedef:** Görüntü verisinden çok sayıda küçük parçacık üretmek.

İşler: - Tek `Particle` modelini uygulamak. - Piksel/alan örnekleme
stratejisini geliştirmek. - Parçacık koordinatlarını ve renk/parlaklık
değerlerini hesaplamak. - Parçacık yoğunluğu ve maksimum parçacık sınırı
eklemek. - Deterministik üretim için seed desteği sağlamak. - Parçacık
verisini doğrulamak.

Çıkış kriteri: - Üretilen parçacıklar kaynak görüntünün ana şekil ve
tonlarını tanınabilir biçimde temsil etmeli.

### Phase 3 --- Animation Engine

**Hedef:** Parçacıkların boş ekrandan başlayarak görüntüyü aşamalı
biçimde oluşturmasını sağlamak.

İşler: - Reveal sıralama algoritması. - Süre, FPS ve gecikme ayarları. -
Opaklık ve parlaklık geçişleri. - Renkli modda koyu tondan kaynak
rengine geçiş. - İsteğe bağlı hareket/titreşim/iz efektleri. - Son
karenin eksiksiz görüntüyü göstermesi.

Çıkış kriteri: - Animasyon başlangıçtan sona kesintisiz ilerlemeli ve
son durumda tam görüntü oluşmalı.

### Phase 4 --- Rendering Layer

**Hedef:** Ortak parçacık ve animasyon verisini farklı hedeflerde
çizilebilir hale getirmek.

İşler: - Ortak render sözleşmesini tanımlamak. - Siyah arka plan ve
ölçekleme kuralları. - Parçacık boyutu ve çizim sırası. - Monochrome ve
color render davranışı. - Render doğruluğu ve performans testleri.

Çıkış kriteri: - Render katmanı işleme ve dışa aktarma mantığından
bağımsız olmalı.

### Phase 5 --- Web Interface

**Hedef:** Kullanıcının görüntü yükleyip ayarları seçebileceği web
arayüzünü oluşturmak.

İşler: - Görüntü yükleme alanı. - Önizleme alanı. - Siyah-beyaz/renkli
çıktı seçimi. - Parçacık yoğunluğu ve animasyon ayarları. -
HTML/terminal format seçimi. - İşleme durumu ve hata mesajları. - Mobil
uyumlu arayüz.

Çıkış kriteri: - Kullanıcı temel akışı arayüz üzerinden
tamamlayabilmeli.

### Phase 6 --- Standalone HTML Export

**Hedef:** Herhangi bir uygulama veya sunucu gerektirmeyen tek HTML
dosyası üretmek.

İşler: - Parçacık verisini dosyaya gömmek. - Çizim ve animasyon kodunu
gömmek. - Otomatik oynatmayı sağlamak. - Responsive canvas/çizim
yüzeyi. - Çevrimdışı çalışma. - Mobil tarayıcı testleri. - Dosya boyutu
ve performans optimizasyonu.

Çıkış kriteri: - Üretilen HTML başka bir cihaza gönderildiğinde,
uygulama kurulmadan açılmalı ve animasyonu oynatmalı.

### Phase 7 --- Terminal Export

**Hedef:** Aynı animasyon verisinden tek dosyalık terminal çıktısı
üretmek.

İşler: - Terminal koordinat/karakter eşlemesi. - Siyah-beyaz ve
destekleniyorsa renkli karakter çıktısı. - Animasyon zamanlaması. -
Windows `.cmd` başlatma akışı. - Terminal boyutu ve ANSI desteği
kontrolleri.

Çıkış kriteri: - Desteklenen Windows ortamında tek `.cmd` dosyası
çalıştırıldığında animasyon başlamalı.

### Phase 8 --- Quality, Optimization and Release

**Hedef:** İlk sürümü güvenilir ve paylaşılabilir hale getirmek.

İşler: - Birim ve entegrasyon testleri. - HTML/terminal veri tutarlılığı
testleri. - Farklı çözünürlüklerde görsel kalite testleri. - Mobil ve
masaüstü performans testleri. - Hata senaryoları ve büyük dosya
testleri. - Kurulum ve kullanım dokümantasyonu. - README ve örnek
çıktılar.

Çıkış kriteri: - Temel kullanım senaryoları tekrar edilebilir, test
edilmiş ve belgelenmiş olmalı.

## 4. Önceliklendirme

Öncelik sırası:

1.  Görüntü işleme doğruluğu
2.  Parçacık kalitesi ve yoğunluğu
3.  Progressive reveal animasyonu
4.  Tek dosyalık mobil uyumlu HTML
5.  Web arayüzü deneyimi
6.  Terminal çıktısı
7.  Ek efektler ve ileri optimizasyonlar

HTML'nin terminalden önce gelmesinin nedeni, çıktının bilgisayarı
olmayan kullanıcılara da kolayca gönderilip açılabilmesidir.

## 5. Test stratejisi

-   Farklı en-boy oranlarına sahip görüntüler.
-   Renkli ve grayscale kaynaklar.
-   Açık, koyu ve yüksek kontrastlı görüntüler.
-   Düşük ve yüksek parçacık yoğunluğu.
-   Küçük ekranlı telefonlar ve masaüstü tarayıcılar.
-   Çevrimdışı HTML açılışı.
-   Aynı ayarlarla tekrarlanabilir çıktı üretimi.
-   Büyük parçacık sayılarında bellek ve kare hızı.

## 6. Kapsam yönetimi

İlk sürümde temel kalite hedefi, kaynak görüntünün çok sayıda küçük
parçacıkla aşamalı biçimde oluşmasıdır. Ses, kullanıcı hesabı, bulut
depolama, sosyal paylaşım platformu entegrasyonu ve gelişmiş düzenleme
özellikleri ilk sürümün zorunlu kapsamına dahil değildir.

Bu yol haritası yaşayan bir belgedir. Aşamaların sırası ancak teknik
bağımlılık veya test sonuçları gerekçelendirdiğinde değiştirilmelidir.
