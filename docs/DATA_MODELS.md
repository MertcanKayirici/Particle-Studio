# Particle Studio --- Veri Modelleri

## 1. Amaç

Bu doküman, Particle Studio'nun Python tabanlı görüntü işleme ve
parçacık motorunda kullanılacak temel veri yapılarını tanımlar. Amaç;
görüntü analizi, parçacık üretimi, animasyon ve dışa aktarma
aşamalarının aynı veri sözleşmeleri üzerinden çalışmasını sağlamaktır.

Bu belge mimari tasarımdır. Alan adları ve tipler uygulama sırasında
kesinleştirilebilir; burada tanımlanan sorumlulukların korunması
esastır.

## 2. Temel tasarım ilkeleri

-   **Tek yapıtaşı:** Görseli oluşturan temel eleman tek bir parçacıktır
    (`Particle`).
-   **Renk esnekliği:** Girdi görüntüsü renkli veya gri tonlamalı
    olabilir. Çıktı modu siyah-beyaz ya da renkli seçilebilir.
-   **Tek animasyon modeli:** HTML ve terminal çıktıları aynı parçacık
    verisini ve aynı animasyon zaman çizelgesini kullanır.
-   **Taşınabilir çıktı:** Dışa aktarılan dosya gerekli veriyi ve
    oynatma mantığını kendi içinde taşır.
-   **Ayrıştırılmış sorumluluklar:** Görüntü, parçacık, animasyon, renk
    ve dışa aktarma verileri birbirinden ayrıdır.

## 3. Temel modeller

### 3.1 ImageSource

Kullanıcının yüklediği kaynak görüntüyü ve görüntü işleme için gerekli
bilgileri temsil eder.

  Alan                 Açıklama
  -------------------- ---------------------------------------------
  `source_id`          Kaynağın benzersiz kimliği
  `width` / `height`   Görüntü boyutları
  `mode`               Kaynak renk modu: RGB, RGBA veya grayscale
  `pixel_data`         İşlenecek piksel verisi
  `metadata`           Dosya türü ve isteğe bağlı kaynak bilgileri

Kaynak görüntü değiştirilmeden saklanabilir; işleme adımları
gerektiğinde normalize edilmiş bir temsil üzerinde yürütülür.

### 3.2 ProcessingConfig

Görüntünün parçacıklara dönüştürülmesinde kullanılacak ayarları taşır.

Önerilen alanlar:

-   `target_width`, `target_height`
-   `sampling_density`
-   `brightness_threshold`
-   `contrast`
-   `gamma`
-   `sharpen_amount`
-   `max_particles`
-   `background_color`
-   `output_color_mode`

Parametrelerin varsayılan değerleri profil/preset katmanında
tanımlanmalıdır; motor içine dağınık sabitler olarak
yerleştirilmemelidir.

### 3.3 Particle

Sistemin tek görsel yapıtaşıdır. Her parçacık, çıktı yüzeyinde çizilecek
küçük bir nokta veya eşdeğer terminal karakteri ile temsil edilir.

  Alan             Açıklama
  ---------------- ----------------------------------------------
  `id`             Benzersiz parçacık kimliği
  `x`, `y`         Normalize edilmiş veya çıktı koordinatları
  `size`           Parçacık boyutu
  `color`          RGB/RGBA renk bilgisi veya gri ton değeri
  `brightness`     Parçacığın görsel parlaklığı
  `opacity`        Görünürlük/alpha değeri
  `depth`          İsteğe bağlı çizim sırası veya katman değeri
  `reveal_order`   Animasyonda görünür olacağı sıra/zaman

Parçacıklar küçük ve yoğun olmalıdır. Görsel kalite, tek tek büyük
noktalar yerine çok sayıda küçük parçacığın birlikte oluşturduğu
yoğunluk ve ton farklılıklarıyla elde edilir.

### 3.4 ParticleSet

Bir görüntüyü oluşturan parçacık koleksiyonudur.

-   Kaynak görüntü kimliğini referans eder.
-   Parçacıkları deterministik bir sırada saklar.
-   Toplam parçacık sayısını ve çıktı boyutlarını taşır.
-   HTML ve terminal dışa aktarıcılarına ortak girdi sağlar.

### 3.5 ColorProfile

Renk üretim ve dönüştürme kurallarını tanımlar.

Desteklenecek çıktı modları:

-   `monochrome`: Siyah arka plan üzerinde beyaz/gri parçacıklar.
-   `color`: Siyah arka plan üzerinde kaynak görüntünün renklerini
    taşıyan parçacıklar.

Renkli modda parçacıklar başlangıçta karanlık veya düşük opaklıkta
görünüp animasyon boyunca gerçek renklerine yaklaşabilir. Siyah-beyaz
modda aynı zamanlama mantığı parlaklık değerlerine uygulanır.

### 3.6 AnimationConfig

Parçacıkların başlangıçtan son görüntüye nasıl ulaşacağını tanımlar.

Önerilen alanlar:

-   `duration_ms`
-   `fps`
-   `start_delay_ms`
-   `reveal_strategy`
-   `order_seed`
-   `fade_in`
-   `brightness_transition`
-   `color_transition`
-   `particle_motion`
-   `hold_final_frame`

İmza animasyon, neredeyse boş/koyu bir ekrandan başlayarak parçacıkların
aşamalı biçimde görünmesi ve sonunda kaynak görüntünün tamamının
oluşmasıdır. Hareket, titreşim veya iz gibi efektler isteğe bağlı
parametrelerdir; temel oluşum animasyonunun yerine geçmez.

### 3.7 ExportConfig

Dışa aktarma hedefini ve dosyanın nasıl üretileceğini tanımlar.

  Alan                               Açıklama
  ---------------------------------- ---------------------------------------
  `format`                           `html` veya `terminal`
  `output_path`                      Üretilecek dosyanın konumu
  `canvas_width` / `canvas_height`   Görsel alan boyutları
  `include_controls`                 Oynatma kontrollerinin dahil edilmesi
  `embed_assets`                     Gerekli verilerin dosyaya gömülmesi
  `mobile_responsive`                HTML çıktısının mobil uyumlu olması

## 4. Veri akışı

1.  `ImageSource` oluşturulur.
2.  `ProcessingConfig` ile görüntü normalize edilir ve analiz edilir.
3.  Örnekleme/yoğunluk kuralları kullanılarak `ParticleSet` üretilir.
4.  Renkler `ColorProfile` üzerinden dönüştürülür.
5.  `AnimationConfig` ile parçacıkların görünme sırası ve geçişleri
    belirlenir.
6.  `ExportConfig` seçilen dışa aktarıcıya iletilir.
7.  HTML veya terminal için tek başına çalışabilen çıktı dosyası
    oluşturulur.

## 5. Doğrulama ve tutarlılık

-   Koordinatlar çıktı sınırları içinde olmalıdır.
-   Parçacık sayısı `max_particles` sınırını aşmamalıdır.
-   Renk kanalları geçerli aralıkta olmalıdır.
-   Animasyon sırası deterministik olmalıdır; aynı seed ve ayarlar aynı
    sonucu üretmelidir.
-   HTML ve terminal çıktılarında aynı `ParticleSet` ve animasyon zaman
    çizelgesi esas alınmalıdır.
-   Eksik veya geçersiz ayarlar dışa aktarma başlamadan doğrulanmalıdır.

## 6. Sürümleme

Dışa aktarılan dosyanın içine bir çıktı şeması sürümü eklenmelidir.
Böylece ileride model alanları değiştiğinde eski çıktılar için uyumluluk
stratejisi geliştirilebilir.

Örnek kavramsal alan: `schema_version`.

## 7. Kapsam dışı

Bu doküman veritabanı şeması, kullanıcı hesabı modeli veya bulut
senkronizasyonu tanımlamaz. İlk sürümün temel odağı yerel işleme ve
paylaşılabilir, bağımsız çıktı dosyalarıdır.
