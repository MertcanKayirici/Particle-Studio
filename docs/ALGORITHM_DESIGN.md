# Particle Studio — Algoritma Tasarımı

> Bu doküman Particle Studio'nun görsel analiz, parçacık/ASCII üretimi ve
> aşamalı animasyon algoritmalarının tasarımını açıklar.
>
> **Durum:** Tasarım aşaması. Burada anlatılan akış, uygulanması planlanan
> algoritmadır; henüz tamamlanmış veya performans testinden geçmiş kod
> olarak değerlendirilmemelidir.
>
> İlgili doküman: [`PROJECT_ARCHITECTURE.md`](PROJECT_ARCHITECTURE.md)

---

## 1. Algoritmanın hedefi

Kaynak bir görseli iki görsel temsil biçiminden biriyle yeniden üretmek:

1. **Particle modu:** Görsel, çok sayıda küçük ve tekil parçacığın
   konumlandırılmasıyla oluşturulur.
2. **ASCII modu:** Görsel, parlaklık/renk bilgisine göre seçilen metin
   karakterleriyle temsil edilir.

Her iki modun da ortak davranışı, görüntünün bir anda gösterilmesi yerine
başlangıçta siyah veya neredeyse boş bir ekrandan başlayıp zaman içinde
oluşmasıdır.

Çıktı rengi ayrıca seçilir:

- **Monochrome:** Siyah-beyaz / gri tonları.
- **Color:** Kaynak görselden türetilen renkler.

Dolayısıyla görsel temsil biçimi ile renk modu birbirinden bağımsız
seçeneklerdir. Örneğin Particle + Color veya ASCII + Monochrome
kullanılabilir.

## 2. Genel işlem hattı

```text
Kaynak görsel
    |
    v
Görseli yükle ve doğrula
    |
    v
Ölçeklendir / en-boy oranını koru
    |
    v
Piksel renklerini ve parlaklığı analiz et
    |
    +------------------------------+
    |                              |
    v                              v
Particle üretimi              ASCII hücre üretimi
    |                              |
    +---------------+--------------+
                    |
                    v
             Renk modunu uygula
                    |
                    v
          Reveal sırasını hesapla
                    |
                    v
          Zaman çizelgesi oluştur
                    |
          +---------+---------+
          |                   |
          v                   v
    HTML animasyon        Terminal kareleri
```

İşlem hattının amacı, görsel analizini ve animasyon verisi üretimini
çıktı biçimlerinden bağımsız tutmaktır. HTML ve terminal dışa aktarıcıları
aynı temel üretim sonucunu kullanmalıdır.

## 3. Görsel ön işleme

### 3.1 Dosya yükleme ve doğrulama

Girdi dosyası yüklenirken:

- Dosya biçimi destekleniyor mu kontrol edilir.
- Görselin genişlik ve yüksekliği okunur.
- Boş veya bozuk dosyalar reddedilir.
- Çok büyük görseller için güvenli bir işleme sınırı uygulanır.
- Görsel, algoritmanın kullanacağı standart piksel temsiline dönüştürülür.

İlk sürümde desteklenecek dosya biçimleri uygulama geliştirilirken
kesinleştirilecektir. JPEG ve PNG başlangıç için uygun adaylardır.

### 3.2 Boyutlandırma

Görsel, kullanıcının seçtiği çıktı genişliği/yüksekliğine veya kalite
profiline göre işlenir.

- En-boy oranı korunur.
- Görsel gereksiz yere esnetilmez.
- İşleme çözünürlüğü, üretilecek parçacık/karakter sayısını doğrudan
  etkiler.
- Mobil ve masaüstü HTML çıktılarında görüntü alanına sığdırma işlemi
  dışa aktarıcı tarafında ayrıca ele alınır.

### 3.3 Renk ve parlaklık analizi

Her piksel için RGB renk bilgisi elde edilir. Parlaklık hesabında
başlangıç yaklaşımı olarak algısal ağırlıklı parlaklık kullanılabilir:

```text
L = 0.2126 * R + 0.7152 * G + 0.0722 * B
```

Burada R, G ve B değerleri 0–1 aralığına normalize edilmiş renk
bileşenleridir.

Bu değer, özellikle siyah-beyaz modda ve ASCII karakteri seçerken
kullanılabilir. Nihai parlaklık dönüşümü görsel testleriyle ayarlanacaktır.

## 4. Particle modu

### 4.1 Temel yapıtaşı

Particle modunda temel yapıtaşı **tekil parçacıktır**. Her parçacık küçük
bir görsel nokta olarak çizilir. Çok sayıda küçük parçacık birlikte
kaynak görselin şeklini ve ayrıntılarını oluşturur.

Parçacıklar büyük lekeler veya geniş hücreler halinde gruplanmamalıdır.
Yoğunluk, küçük parçacıkların sayısı artırılarak elde edilmelidir.

### 4.2 Parçacık konumlarının belirlenmesi

İlk sürüm için uygulanabilir yaklaşım, işlenmiş görsel üzerinde aday
konumlar oluşturmaktır.

Olası stratejiler:

- **Uniform sampling:** Görsel alanına düzenli aralıklı aday noktalar
  yerleştirmek.
- **Random sampling:** Görsel alanından rastgele aday noktalar seçmek.
- **Brightness/density sampling:** Parlaklık veya kontrast bilgisine
  göre bazı bölgelerde daha sık aday nokta üretmek.

Başlangıç uygulamasında algoritma basit ve ölçülebilir tutulmalıdır.
Önce uniform veya kontrollü random sampling uygulanıp sonuçlar
gözlemlenebilir; daha gelişmiş yoğunluk dağılımı sonraki iyileştirme
olarak eklenebilir.

### 4.3 Parçacık özellikleri

Bir parçacığın veri modeli en az şu bilgileri taşımalıdır:

| Alan | Açıklama |
|---|---|
| `x` | Normalize yatay konum |
| `y` | Normalize dikey konum |
| `r`, `g`, `b` | Kaynak görselden türetilen renk |
| `brightness` | Parlaklık değeri |
| `reveal_order` | Animasyonda görünme sırası |

Parçacık boyutu ve opaklık gibi çizim özellikleri de gerekebilir.
Bunların veri modelinde mi yoksa render ayarlarında mı tutulacağı
uygulama sırasında netleştirilecektir.

### 4.4 Renk modu

**Monochrome:**

- Parçacık rengi, piksel parlaklığından türetilen gri tona çevrilir.
- Siyah arka plan üzerinde açık tonlu parçacıklar görüntüyü oluşturur.

**Color:**

- Parçacık, kaynak görseldeki karşılık gelen konumun rengini alır.
- Animasyon başında parçacıklar görünürken renkleri düşük yoğunlukta
  olabilir.
- İlerleyen aşamalarda renkler nihai değerlerine doğru açılabilir.

Renk açılması animasyonun bir parçasıdır; kaynak görselin renk bilgisini
değiştiren ayrı bir filtre olarak düşünülmemelidir.

## 5. ASCII modu

### 5.1 Hücre tabanlı temsil

ASCII modunda görsel, karakter hücrelerinden oluşan bir ızgaraya
dönüştürülür. Her hücre kaynak görselin ilgili alanını temsil eder.

Her hücre için ortalama parlaklık hesaplanır ve parlaklık seviyesine
uygun bir karakter seçilir.

### 5.2 Karakter rampası

Karakter rampası, koyu alanlardan açık alanlara doğru görsel yoğunluğu
artan karakterlerden oluşur. Örnek bir başlangıç rampası:

```text
 .:-=+*#%@
```

Karakter sıralaması kullanılan yazı tipi ve çıktı ortamına göre test
edilmelidir. Terminal ve HTML'de aynı karakterler farklı görsel
yoğunlukta algılanabilir.

### 5.3 Renkli ASCII

Color modunda karakter rengi ilgili hücrenin kaynak görselinden
türetilir. Monochrome modunda hücre parlaklığı gri ton olarak kullanılır.

HTML çıktısında renkli karakterlerin ayrı ayrı stillenmesi dosya boyutunu
artırabilir. Bu nedenle dışa aktarma aşamasında veri boyutu ve çizim
performansı ölçülmelidir.

### 5.4 Terminal uyumu

Terminalde karakter hücreleri kare değildir. Bu nedenle ASCII çıktısının
en-boy oranı, terminal karakter hücrelerinin yaklaşık genişlik/yükseklik
oranı dikkate alınarak düzeltilmelidir.

Terminal boyutu küçükse çıktı genişliği sınırlandırılmalı veya kullanıcıya
uygun bir çözünürlük seçilmelidir.

## 6. Aşamalı oluşum (progressive reveal)

### 6.1 Temel davranış

Animasyonun başlangıç karesi siyah veya neredeyse boş olmalıdır.
Parçacıklar ya da ASCII hücreleri belirlenen sırayla görünür hale gelir.
Son karede görselin tamamı oluşmuş olmalıdır.

### 6.2 Reveal sıralaması

Her öğeye bir `reveal_order` değeri atanır. Bu değer öğenin animasyonda
hangi sırada görünür olacağını belirler.

Değerlendirilecek sıralama stratejileri:

- Rastgele sırayla ortaya çıkma.
- Merkezden dışa doğru yayılma.
- Dış kenarlardan merkeze doğru oluşma.
- Satır/sütun veya tarama düzeninde oluşma.
- Görsel bölgelerine göre kontrollü karışık sıra.

İlk sürümde bir temel sıralama stratejisi uygulanmalı; diğerleri daha
sonra efekt seçeneği olarak eklenmelidir. Nihai varsayılan strateji,
görsel örnekleri üzerinde karşılaştırma yapıldıktan sonra seçilecektir.

### 6.3 Zaman çizelgesi

Reveal sırası, toplam animasyon süresiyle ilişkilendirilir.

Basit model:

```text
progress = elapsed_time / duration
visible_count = progress * total_item_count
```

`progress` 0 ile 1 arasında sınırlandırılır. `visible_count`, ilgili
zamana kadar görünmesi gereken öğe sayısını belirtir.

Daha sonra easing veya farklı hız eğrileri eklenebilir. Örneğin
başlangıçta yavaş, ortada hızlı, sona doğru tekrar yavaş bir oluşum
sağlanabilir.

### 6.4 Parçacıkların görünme biçimi

Bir öğe kendi reveal zamanına ulaştığında:

- Görünür hale gelebilir.
- Kısa bir opacity geçişi yapabilir.
- Küçük bir parlaklık artışıyla belirginleşebilir.

Bu davranışlar performans maliyeti ve görsel kalite açısından test
edilmelidir. İlk hedef, çok sayıda öğenin akıcı biçimde ortaya çıkmasıdır.

### 6.5 Renklerin açılması

Renkli modda iki aşamalı bir görünüm değerlendirilecektir:

1. Parçacık/karakter görünmeye başlar.
2. Renk, düşük yoğunluk veya soluk bir tondan kaynak rengin nihai
   değerine doğru geçiş yapar.

Siyah-beyaz modda renk geçişi yerine parlaklık/opacity geçişi uygulanır.

## 7. Animasyon verisi ve çıktıdan bağımsızlık

Üretim motoru, doğrudan HTML veya terminal kodu üretmek yerine ortak bir
animasyon veri yapısı hazırlamalıdır.

Örnek kavramsal veri:

```json
{
  "width": 1000,
  "height": 750,
  "mode": "particle",
  "color_mode": "color",
  "duration_ms": 6000,
  "background": "#000000",
  "items": [
    {
      "x": 0.42,
      "y": 0.31,
      "color": [230, 190, 210],
      "brightness": 0.78,
      "reveal_order": 120
    }
  ]
}
```

Bu örnek yalnızca veri yapısının anlatımı içindir; nihai şema değildir.
Gerçek alan adları ve serileştirme biçimi `DATA_MODELS.md` içinde
kesinleştirilecektir.

Ortak veri sayesinde:

- HTML dışa aktarıcı aynı animasyon verisini kullanır.
- Terminal dışa aktarıcı aynı reveal sırasını kullanır.
- Görsel analizi her çıktı türü için tekrar çalıştırılmaz.
- Yeni çıktı biçimleri eklemek kolaylaşır.

## 8. HTML ve terminal oynatma farkı

### HTML

- Animasyon tarayıcıda oynatılır.
- Tek dosyalık HTML içine gerekli stil, JavaScript ve animasyon verisi
  gömülür.
- Mobil ekran boyutlarına uyum sağlanır.
- Harici sunucu veya Python kurulumu gerektirmemesi hedeflenir.
- Animasyon, dosya açıldığında otomatik başlayacak şekilde tasarlanır;
  tarayıcı kısıtları nedeniyle ses gibi ek özellikler varsa kullanıcı
  etkileşimi gerekebilir.

### Terminal

- Animasyon zaman aralıklarıyla kare kare oynatılır.
- Terminal ekranı temizlenerek veya imleç konumu güncellenerek yeni
  kare gösterilir.
- Terminalin desteklediği renk modu ve karakter genişliği dikkate alınır.
- Terminal çıktısı, HTML dosyası kadar platform bağımsız değildir.

## 9. Performans ve kalite ölçütleri

Algoritma geliştirilirken şu ölçütler takip edilmelidir:

- Parçacık/karakter sayısı.
- Üretim süresi.
- Animasyon verisinin dosya boyutu.
- HTML dosyasının açılma süresi.
- Masaüstü tarayıcıda oynatma akıcılığı.
- Mobil tarayıcıda oynatma akıcılığı.
- Son karede kaynak görselin tanınabilirliği.
- Küçük parçacıkların ayrıntıları koruyabilmesi.
- Renk geçişlerinin görsel kalitesi.

İlk testlerde düşük, orta ve yüksek yoğunluk profilleri kullanılabilir.
Kesin parçacık sayısı ve çözünürlük limitleri ölçüm yapılmadan
sabitlenmemelidir.

## 10. Geliştirme sırası

1. Görsel yükleme ve doğrulama.
2. Görseli standart boyuta dönüştürme.
3. Basit Particle üretimi.
4. Monochrome Particle önizlemesi.
5. Reveal sıralaması ve aşamalı animasyon.
6. Renkli Particle modu ve renk açılması.
7. ASCII üretimi.
8. Monochrome ve Color ASCII modları.
9. Ortak animasyon veri modelinin kesinleştirilmesi.
10. Tek dosyalık HTML dışa aktarıcı.
11. Mobil tarayıcı testleri.
12. Terminal dışa aktarıcı.
13. Performans ve kalite iyileştirmeleri.

Bu sıra, temel görsel üretim algoritmasının erken aşamada doğrulanmasını
ve dışa aktarma işlerinin kararlı veri modeli üzerine kurulmasını sağlar.

---

## 11. Açık teknik kararlar

Aşağıdaki konular henüz kesinleştirilmemiştir ve prototip/test
sonuçlarına göre karara bağlanmalıdır:

- Parçacık konumları için varsayılan sampling stratejisi.
- Parçacık yoğunluğunun parlaklıkla ilişkisi.
- Reveal sıralamasının varsayılan türü.
- Parçacık opacity/scale geçişlerinin kullanımı.
- Renk açılmasının süresi ve easing eğrisi.
- HTML animasyonunda Canvas veya SVG gibi çizim yaklaşımının seçimi.
- Mobil cihazlar için güvenli öğe sayısı ve çözünürlük sınırları.
- ASCII karakter rampasının ve terminal renk desteğinin kapsamı.

Bu kararlar, küçük prototipler ve gerçek cihaz testleriyle verilmelidir.
