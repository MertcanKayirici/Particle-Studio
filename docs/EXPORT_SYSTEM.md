# Particle Studio --- Dışa Aktarma Sistemi

## 1. Amaç

Dışa aktarma sistemi, Python motorunun ürettiği parçacık verisini
kullanıcı tarafından seçilen biçimde paylaşılabilir bir dosyaya
dönüştürür. İlk sürümün öncelikli hedefi, alıcının Particle Studio'yu
veya Python'ı kurmasına gerek kalmadan açabileceği tek dosyalık HTML
çıktısıdır. Terminal çıktısı ikincil hedeftir.

## 2. Desteklenecek formatlar

### 2.1 Standalone HTML

Birincil paylaşım formatıdır.

-   Tek bir `.html` dosyası olarak üretilir.
-   CSS, JavaScript, parçacık verisi ve oynatma ayarları dosyanın içine
    gömülür.
-   Harici sunucu, Python kurulumu veya ek asset klasörü gerektirmez.
-   Masaüstü ve mobil tarayıcılarda çalışacak şekilde responsive
    tasarlanır.
-   Dosya WhatsApp gibi mesajlaşma uygulamalarıyla paylaşılabilir; alıcı
    dosyayı cihazında tarayıcıyla açabilir.

HTML çıktısı açıldığında animasyon otomatik başlamalıdır. İsteğe bağlı
olarak tekrar oynatma ve duraklatma kontrolleri sunulabilir.

### 2.2 Terminal çıktısı

İkincil ve daha sınırlı bir çıktı biçimidir.

-   Tek bir çalıştırılabilir `.cmd` dosyası hedeflenir.
-   Dosya Windows CMD ortamında açılarak animasyonu terminalde oynatır.
-   Terminal karakterleri ve ANSI renk desteği ortamın yeteneklerine
    göre kullanılmalıdır.
-   Terminal çıktısı mobil cihazlarda HTML kadar erişilebilir değildir;
    bu nedenle ana paylaşım formatı olarak değerlendirilmez.

Not: `.cmd` Windows'a özgüdür. Linux ve macOS terminal desteği ileride
ayrı bir çalıştırma biçimi veya uyumlu launcher gerektirebilir. Tek
dosya şartı korunarak platform desteği ayrıca doğrulanmalıdır.

## 3. Ortak çıktı sözleşmesi

HTML ve terminal dışa aktarıcıları aynı temel veriyi kullanmalıdır:

-   Parçacık koordinatları ve renkleri
-   Parçacıkların görünme sırası
-   Animasyon süresi ve kare/zamanlama bilgisi
-   Arka plan rengi
-   Çıktı boyutları
-   Renk modu
-   Şema sürümü

Dışa aktarıcılar görüntüyü yeniden analiz etmemeli veya kendi
parçacıklarını üretmemelidir. Bu işlemler Python çekirdeğinin
sorumluluğudur.

## 4. HTML dosyasının içeriği

Tek dosyalık HTML çıktısı kavramsal olarak şu bölümleri içerir:

1.  HTML belge iskeleti
2.  Responsive stil tanımları
3.  Canvas veya uygun çizim yüzeyi
4.  Gömülü parçacık verisi
5.  Animasyon oynatma kodu
6.  Başlangıç/son durum ve oynatma ayarları
7.  İsteğe bağlı kullanıcı kontrolleri

Çıktı dosyası üretildikten sonra kaynak görselin veya uygulamanın
çalışma klasörünün varlığına bağımlı olmamalıdır.

## 5. Animasyon davranışı

Her iki çıktı biçiminde hedeflenen görsel akış:

1.  Siyah veya çok koyu, neredeyse boş ekran.
2.  İlk parçacıkların yavaşça görünmeye başlaması.
3.  Parçacık yoğunluğunun ve görünür alanın kademeli artması.
4.  Ana objenin silüet ve ayrıntılarının belirginleşmesi.
5.  Parçacıkların son parlaklıklarına ve renklerine ulaşması.
6.  Tam görüntünün ekranda sabit kalması.

Siyah-beyaz modda parlaklık kademeli yükselir. Renkli modda parçacıklar
koyu başlangıç tonlarından kaynak renklerine geçebilir. Her iki mod da
aynı reveal zaman çizelgesini kullanır.

## 6. Mobil uyumluluk

HTML çıktısı için zorunlu tasarım hedefleri:

-   Ekran genişliğine göre ölçeklenen çizim alanı
-   Dikey ve yatay yön desteği
-   Dokunmatik cihazlarda rahat açılma ve görüntülenme
-   Farklı piksel yoğunluklarına uyum
-   Küçük ekranlarda taşma veya yatay kaydırma oluşturmama
-   Animasyon performansı için parçacık sayısı ve çizim yükünün kontrolü

Mobil performans, masaüstü performansından ayrı test edilmelidir.

## 7. Performans ve dosya boyutu

-   Parçacık verisi gereksiz tekrarlar olmadan serileştirilmelidir.
-   Uygun olduğunda sayısal veriler kompakt biçimde saklanmalıdır.
-   HTML dosyası kendi kendine yeterli kalırken dosya boyutu makul
    tutulmalıdır.
-   Kare başına tüm parçacıkları yeniden hesaplamak yerine mümkün
    olduğunda önceden hazırlanmış veriler kullanılmalıdır.
-   Yüksek parçacık sayılarında hedef cihazın bellek ve çizim kapasitesi
    dikkate alınmalıdır.

## 8. Hata yönetimi

Dışa aktarma öncesinde format, hedef yol, veri bütünlüğü ve parçacık
sayısı doğrulanmalıdır. Yazma hatalarında kullanıcıya anlaşılır hata
verilmeli; yarım veya bozuk dosya başarılı çıktı olarak
gösterilmemelidir.

## 9. Kabul kriterleri

-   HTML çıktısı tek dosyadır ve çevrimdışı açılabilir.
-   HTML dosyası masaüstü ve mobil tarayıcıda çalışır.
-   Animasyon kullanıcıdan ek kurulum istemeden başlar.
-   Terminal çıktısı desteklenen Windows ortamında tek `.cmd` dosyası
    olarak çalışır.
-   İki çıktı biçimi aynı parçacık verisini ve aynı animasyon sırasını
    temel alır.
-   Siyah-beyaz ve renkli modlar desteklenir.
