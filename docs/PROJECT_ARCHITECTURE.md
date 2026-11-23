# Particle Studio --- Proje Genel Bakış ve Mimari Tasarım

> Bu doküman projenin amacını, temel ürün kararlarını, mimari
> katmanlarını, modüllerin sorumluluklarını ve veri akışını açıklar.\
> **Ana `README.md` değildir.** Ana README, proje işlevleri
> tamamlandıkça ve gerçek kullanım netleştikçe hazırlanacaktır.

## 1. Projenin amacı

Particle Studio, kullanıcının seçtiği bir görseli parçacıklar veya ASCII
karakterler kullanarak yeniden oluşturan ve bu oluşumu animasyon halinde
dışa aktarabilen bir uygulamadır.

Uygulamanın ayırt edici özelliği yalnızca fotoğrafı parçacıklara
dönüştürmek değildir. Görsel, başlangıçta tamamen siyah veya neredeyse
boş bir ekrandan başlayarak zaman içinde aşamalı biçimde ortaya çıkar.
Animasyon tamamlandığında kaynak görsel, seçilen görsel stile göre
tanınabilir ve mümkün olduğunca ayrıntılı hale gelir.

Üretilen animasyonun kolayca paylaşılması temel ürün hedeflerinden
biridir. Bu nedenle öncelikli çıktı, tek başına çalışabilen bir HTML
dosyasıdır. Bu dosya başka bir kişiye mesajlaşma uygulamaları üzerinden
gönderilebilir ve modern bir tarayıcıda açıldığında animasyonu
oynatabilir.

## 2. Temel ürün kararları

  -----------------------------------------------------------------------
  Alan                                Karar
  ----------------------------------- -----------------------------------
  Görüntü işleme motoru               Python

  Kullanıcı arayüzü                   Web tabanlı

  Temel görsel yapıtaşı               Tekil parçacık (single particle)

  Girdi görselleri                    Renkli veya siyah-beyaz

  Çıktı renk modu                     Renkli veya siyah-beyaz

  Görsel üretim yöntemi               Parçacık veya ASCII

  Ana animasyon                       Tam aşamalı oluşum (full
                                      progressive reveal)

  Varsayılan arka plan                Siyah

  Öncelikli çıktı                     Tek dosyalık bağımsız HTML

  İkincil çıktı                       Terminal/CMD animasyonu

  Hedef cihazlar                      Mobil ve masaüstü tarayıcıları;
                                      terminal çıktısı için desteklenen
                                      masaüstü terminalleri
  -----------------------------------------------------------------------

Bu kararlar projenin başlangıç mimarisini belirler. İleride yeni
efektler veya çıktı türleri eklenebilir; ancak temel parçacık modeli ve
bağımsız HTML çıktısı korunmalıdır.

## 3. Kullanıcı deneyimi

Öngörülen temel kullanım akışı şöyledir:

1.  Kullanıcı uygulamayı açar.
2.  Bir görsel yükler.
3.  Görsel üretim yöntemini seçer: parçacık veya ASCII.
4.  Çıktı renk modunu seçer: renkli veya siyah-beyaz.
5.  Görsel yoğunluğu, parçacık boyutu, animasyon süresi ve benzeri
    ayarları düzenler.
6.  Önizlemeyi oluşturur ve sonucu kontrol eder.
7.  Çıktı türünü seçer.
8.  Uygulama animasyonu dışa aktarır.

Kullanıcının arkadaşına göndereceği temel çıktı tek bir HTML dosyasıdır.
Dosyayı alan kişinin Python, Particle Studio veya başka bir geliştirme
aracı kurması gerekmemelidir.

## 4. Görsel üretim davranışı

### 4.1 Parçacık modu

Parçacık modunda görsel, çok sayıda küçük parçacığın bir araya
gelmesiyle oluşturulur.

-   Parçacıklar küçük olmalı; görüntü çok sayıda parçacık sayesinde
    ayrıntı kazanmalıdır.
-   Parçacıkların konumları ve görsel özellikleri kaynak görselden
    türetilmelidir.
-   Parçacıkların rengi, seçilen çıktı moduna göre kaynak görselin
    renklerinden veya parlaklık değerlerinden belirlenmelidir.
-   Parçacıkların görünme sırası animasyonun parçasıdır.
-   Yoğunluk ve parçacık boyutu ayarlanabilir olmalıdır.

### 4.2 ASCII modu

ASCII modunda görsel, parlaklık ve gerektiğinde renk değerlerine göre
seçilen karakterlerle temsil edilir.

-   Karakter yoğunluğu görselin ayrıntı seviyesini etkiler.
-   Koyu ve açık alanlar farklı karakterlerle ifade edilir.
-   Terminal çıktısı, terminalin karakter hücresi oranını dikkate
    almalıdır.
-   HTML çıktısında ASCII görünümü, mobil ekranlarda taşma oluşturmadan
    ölçeklenebilmelidir.

### 4.3 Aşamalı oluşum animasyonu

Ana efekt, görselin baştan sona aşamalı biçimde ortaya çıkmasıdır.

1.  Animasyon siyah veya neredeyse boş bir ekranla başlar.
2.  İlk parçacıklar/karakterler görünür.
3.  Yeni parçacıklar belirerek ana şekli oluşturmaya başlar.
4.  Görselin ayrıntıları giderek belirginleşir.
5.  Animasyon tamamlandığında görselin tamamı görünür hale gelir.

Renkli modda yalnızca parçacıkların görünmesi değil, renklerin de zaman
içinde belirginleşmesi sağlanabilir. Örneğin siyah arka plan üzerinde
ana obje önce soluk/parlaklığı düşük görünür, ardından gerçek renklerine
doğru açılır.

## 5. Yüksek seviyeli mimari

Mimari, sorumlulukları birbirinden ayrılmış katmanlardan oluşur:

``` text
                 KULLANICI
                     |
                     v
          WEB KULLANICI ARAYÜZÜ
          - Görsel yükleme
          - Ayarların seçilmesi
          - Önizleme
          - Dışa aktarma isteği
                     |
                     v
             PYTHON MOTORU
          - Görsel yükleme
          - Görsel analizi
          - Parçacık üretimi
          - Reveal sıralaması
          - Animasyon verisi
                     |
             +-------+-------+
             |               |
             v               v
      HTML DIŞA AKTARMA   TERMİNAL DIŞA AKTARMA
      - CSS               - ASCII kareleri
      - JavaScript        - Zamanlama
      - Animasyon verisi  - Terminal oynatma
             |               |
             v               v
       TEK HTML DOSYASI   TERMİNAL ÇIKTISI
```

### 5.1 Web arayüzü

Web arayüzü kullanıcıyla etkileşimi yönetir. Görsel yükleme, ayarların
seçilmesi, önizleme ve dışa aktarma işlemlerini sunar.

Arayüz, parçacık üretim algoritmalarını kendi içinde yeniden
uygulamamalıdır. Görsel işleme ve animasyon verisi üretme sorumluluğu
Python motorunda kalmalıdır.

### 5.2 Python motoru

Python motoru uygulamanın işlem merkezidir. Kaynak görseli analiz eder,
parçacıkları üretir, parçacıkların görünme sırasını belirler ve dışa
aktarıcıların kullanacağı animasyon verisini hazırlar.

Motorun web arayüzünden ve çıktı biçimlerinden bağımsız tutulması
hedeflenir. Böylece aynı üretim mantığı hem HTML hem terminal çıktısında
kullanılabilir.

### 5.3 Dışa aktarma katmanı

Dışa aktarma katmanı, motorun hazırladığı ortak animasyon verisini hedef
çıktı biçimine dönüştürür.

**HTML dışa aktarıcı:** - Tek bir `.html` dosyası üretir. - Gerekli CSS
ve JavaScript kodunu dosyanın içine gömer. - Animasyon verisini dosyanın
içine ekler. - Harici kütüphane, sunucu veya internet bağlantısına
bağımlı olmadan çalışmayı hedefler. - Mobil ve masaüstü ekranlarına uyum
sağlar.

**Terminal dışa aktarıcı:** - ASCII karelerini zaman sırasına göre
oynatır. - Terminal ekranını güncelleyerek aşamalı oluşum efektini
gösterir. - Terminal boyutları ve karakter hücresi oranları için uygun
davranış sağlamalıdır.

## 6. Python paket ve modül sorumlulukları

Planlanan kaynak kod yapısı:

``` text
src/
└── particle_studio/
    ├── core/
    │   └── models.py
    ├── imaging/
    │   ├── loader.py
    │   └── analysis.py
    ├── particles/
    │   └── generator.py
    ├── animation/
    │   └── reveal.py
    ├── rendering/
    │   ├── ascii_renderer.py
    │   └── particle_renderer.py
    ├── exporters/
    │   ├── html_exporter.py
    │   └── terminal_exporter.py
    ├── config.py
    └── __main__.py
```

  -----------------------------------------------------------------------
  Modül                               Sorumluluk
  ----------------------------------- -----------------------------------
  `core/`                             Modüller arasında paylaşılacak
                                      temel veri modelleri

  `imaging/`                          Görsel dosyasını yükleme, doğrulama
                                      ve analiz etme

  `particles/`                        Görsel verisinden tekil parçacıklar
                                      üretme

  `animation/`                        Parçacıkların/karakterlerin görünme
                                      sırasını ve zaman çizelgesini
                                      hazırlama

  `rendering/`                        Parçacık ve ASCII önizleme/çizim
                                      işlemleri

  `exporters/`                        Ortak animasyon verisini HTML veya
                                      terminal çıktısına dönüştürme

  `config.py`                         Uygulama ve üretim varsayılanları

  `__main__.py`                       Uygulamanın komut satırından
                                      başlatılması
  -----------------------------------------------------------------------

### 6.1 Ortak veri modeli

Parçacık, motorun temel görsel yapıtaşıdır. Bir parçacık en azından şu
bilgileri taşıyabilir:

-   Normalize edilmiş X ve Y konumu
-   Kırmızı, yeşil ve mavi renk bileşenleri
-   Parlaklık değeri
-   Animasyonda görünme sırası

Animasyon verisi, dışa aktarıcıların kullanabileceği biçimde
düzenlenmelidir. Böylece HTML ve terminal dışa aktarıcıları görüntü
analizini ve parçacık üretimini tekrar etmek zorunda kalmaz.

Veri modelinin nihai alanları performans ve animasyon ihtiyaçları test
edildikçe geliştirilebilir.

## 7. Teknoloji seçimi

  Teknoloji      Kullanım amacı
  -------------- ------------------------------------------------------
  Python 3.11+   Görüntü işleme ve üretim motoru
  Pillow         Görsel dosyalarını açma ve temel görüntü işlemleri
  NumPy          Piksel, renk, parlaklık ve örnekleme hesaplamaları
  HTML           Paylaşılabilir çıktı ve web arayüzü
  CSS            Arayüz ve çıktı görünümü
  JavaScript     HTML çıktısının animasyon oynatımı
  Canvas         Tarayıcıda çok sayıda parçacığı verimli çizme hedefi
  Pytest         Otomatik testler
  Ruff           Python kod kalitesi ve biçim denetimi

Tek dosyalık HTML çıktısında çalışma zamanında harici JavaScript/CSS
kütüphanesi yüklenmemesi hedeflenir. Bu, dosyanın çevrimdışı ve paylaşım
sonrasında bağımsız çalışmasını kolaylaştırır.

## 8. Veri akışı

Örnek parçacık modu akışı:

1.  Görsel yükleyici kaynak dosyayı açar ve desteklenen ortak renk
    biçimine dönüştürür.
2.  Görsel analiz modülü piksel, parlaklık, renk ve gerekirse kenar
    bilgilerini çıkarır.
3.  Parçacık üreticisi analiz verisinden parçacık konumlarını ve görsel
    özelliklerini oluşturur.
4.  Animasyon modülü parçacıkların görünme sırasını ve zamanlamasını
    belirler.
5.  Önizleme motoru sonucu uygulama içinde gösterir.
6.  Kullanıcı HTML dışa aktarmayı seçerse HTML dışa aktarıcı animasyon
    verisini, CSS'i ve JavaScript oynatıcısını tek dosyada birleştirir.
7.  Dosya tarayıcıda açıldığında animasyon, gömülü veriler üzerinden
    oynatılır.

ASCII modu da aynı genel akışı izler; ancak görsel temsil parçacıklar
yerine karakterlerden oluşur.

## 9. Bağımsız HTML çıktısı için zorunlu koşullar

HTML dosyası projenin en önemli teslim biçimidir. Bu nedenle şu koşullar
tasarımın başından itibaren dikkate alınmalıdır:

-   Tek dosya olarak paylaşılabilmeli.
-   CSS, JavaScript ve animasyon verisi dosyanın içinde bulunmalı.
-   Python veya yerel bir sunucu gerektirmemeli.
-   İnternet bağlantısı olmadan açılabilmeli.
-   Android ve iOS tarayıcılarında kullanılabilir olmalı.
-   Windows ve Linux masaüstü tarayıcılarında çalışmalı.
-   Farklı ekran boyutlarına uyum sağlamalı.
-   Animasyon başlatma ve oynatma davranışı tarayıcı kısıtlarıyla uyumlu
    olmalı.
-   Büyük animasyon verilerinde dosya boyutu ve bellek kullanımı kontrol
    altında tutulmalı.

Özellikle mobil tarayıcı performansı, parçacık sayısı ve animasyon
karelerinin nasıl kodlanacağı konusunda gerçek cihaz testleriyle
doğrulanmalıdır.

## 10. Performans ve kalite hedefleri

-   Çok sayıda küçük parçacıkla ayrıntılı görüntü oluşturabilmek.
-   Parçacık sayısı arttığında bellek tüketimini kontrol edebilmek.
-   Animasyonun başlangıç, orta ve bitiş aşamalarını tutarlı göstermek.
-   Renkli ve siyah-beyaz modları aynı üretim altyapısıyla desteklemek.
-   HTML dosyasını gereksiz yere büyütmemek.
-   Mobil cihazlarda kabul edilebilir akıcılık sağlamak.
-   Modülleri birbirinden bağımsız test edebilmek.

Kesin parçacık sınırları, çözünürlükler ve hedef kare hızları performans
ölçümleri sonrasında belirlenecektir.

## 11. Geliştirme aşamaları

1.  **Proje temeli:** Paket yapısı, yapılandırma ve ortak veri
    modelleri.
2.  **Görsel yükleme:** Dosya doğrulama ve standart görüntü biçimine
    dönüştürme.
3.  **Görsel analizi:** Parlaklık, renk ve örnekleme verilerinin
    çıkarılması.
4.  **Parçacık üretimi:** Tekil parçacıkların konum, renk ve parlaklık
    değerlerinin oluşturulması.
5.  **Aşamalı animasyon:** Boş ekrandan tam görsele geçiş sırasının
    hazırlanması.
6.  **ASCII üretimi:** Karakter tabanlı görsel temsil.
7.  **Önizleme:** Üretilen animasyonun uygulama içinde gösterilmesi.
8.  **HTML dışa aktarma:** Bağımsız ve tek dosyalık animasyon çıktısı.
9.  **Uyumluluk ve optimizasyon:** Mobil/masaüstü tarayıcı testleri ve
    performans iyileştirmeleri.
10. **Terminal çıktısı:** ASCII animasyonunun terminalde oynatılması.
11. **Arayüz entegrasyonu:** Kullanıcı arayüzü ile Python motorunun
    birleştirilmesi.

## 12. Henüz kesinleştirilmemiş teknik konular

Aşağıdaki konular, ihtiyaç ve test sonuçlarına göre
kararlaştırılacaktır:

-   Web arayüzünün Python motoruyla iletişim yöntemi: yerel API, başka
    bir yerel iletişim katmanı veya paketlenmiş çalışma biçimi.
-   Önizleme için kullanılacak kesin çizim ve veri aktarım yöntemi.
-   Parçacıkların görünme sırasını belirleyen algoritmanın ayrıntıları.
-   Animasyon verisinin HTML içinde saklanma ve sıkıştırılma biçimi.
-   Terminal çıktısının tek dosyalı mı yoksa yardımcı çalışma zamanı
    gerektiren bir biçimde mi sunulacağı.
-   Büyük görseller için çözünürlük, parçacık limiti ve kalite
    profilleri.

Bu konular, temel modüller geliştirildikçe ve prototipler test edildikçe
karara bağlanacaktır.

## 13. Mimari ilkeler

1.  **Tek sorumluluk:** Her modül belirli bir işi yapar.
2.  **Bağımsız motor:** Görüntü işleme kodu arayüz koduna bağlanmaz.
3.  **Ortak animasyon verisi:** Farklı dışa aktarıcılar aynı üretim
    çıktısını kullanır.
4.  **Bağımsız çıktı:** HTML dosyasını alan kişi geliştirme ortamına
    ihtiyaç duymaz.
5.  **Ölçerek optimize etme:** Parçacık sayısı ve kare hızı tahminle
    değil, testlerle belirlenir.
6.  **Aşamalı geliştirme:** Önce doğru üretim algoritması, ardından
    arayüz ve dışa aktarma entegrasyonu tamamlanır.

------------------------------------------------------------------------

**Doküman durumu:** Mimari taslak. Uygulama geliştikçe gerçek davranış
ve alınan teknik kararlarla güncellenecektir.
