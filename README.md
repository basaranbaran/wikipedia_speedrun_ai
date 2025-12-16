# 🏎️ Wikipedia Speedrun AI (Local LLM & SBERT)

**[Türkçe Dokümantasyon için tıklayın](#türkçe-dokümantasyon)** | **[📖 English Documentation](#-overview)** | **[📊 Video Karşılaştırması](COMPARISON.md)**

A Tool-Assisted Speedrun (TAS) bot for the Wikipedia Game that uses local AI models to navigate from a random Wikipedia page to a target page by clicking only links, without going back.

This project runs entirely **offline** using your GPU, combining **Semantic Search (SBERT)** for filtering and **Large Language Models (Llama 3.1 via Ollama)** for logical reasoning.

## 📋 Table of Contents

- [Overview](#-overview)
- [Methodologies Compared](#-methodologies-compared)
- [Prerequisites](#️-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [Troubleshooting](#-troubleshooting)
- [Video Comparison](COMPARISON.md)

## 🎯 Overview

The Wikipedia Game is a challenge where you start at a random Wikipedia article and try to reach a target article by only clicking links. This project automates this process using three different AI-powered approaches, comparing their performance across various scenarios.

**Key Features:**
- 🚀 Fully offline operation (no API keys required)
- 🧠 Hybrid AI approach combining semantic search and LLM reasoning
- ⚡ Multiple algorithms for different speed/accuracy trade-offs
- 📊 Comparative performance analysis
- 🎮 Pre-configured challenging scenarios

## 🧠 Methodologies Compared

The project implements and compares three different algorithmic approaches:

### 1. Hybrid Standard (The Champion 🏆)
**File:** `method_1.py`

- **Logic:** Uses SBERT to find the top 10 mathematically closest links, then asks **Llama 3.1** to pick the most logical one.
- **Pros:** 
  - Fast (3-5s per step)
  - Context-aware
  - Avoids common semantic traps (e.g., "White House" vs "White House painting")
- **Cons:** Slightly slower than pure vector-based approach

### 2. Pure SBERT (Speed Demon ⚡)
**File:** `method_2.py`

- **Logic:** Calculates Cosine Similarity between the target vector and link vectors. Picks the #1 mathematically closest link immediately.
- **Pros:** 
  - Extremely fast (<1s per step)
  - No LLM overhead
- **Cons:** 
  - Context-blind
  - Easily trapped by homonyms (words that look alike but mean different things)

### 3. Chain-of-Thought (The Professor)
**File:** `method_3.py`

- **Logic:** Filters top 5 links, then asks Llama 3.1 to **explain its reasoning** before selecting a link.
- **Pros:** 
  - Highest potential accuracy for complex, indirect connections
  - Transparent decision-making process
- **Cons:** 
  - Slowest due to token generation for explanations
  - Often "overthinks" simple paths

## 🛠️ Prerequisites

Before you begin, ensure you have:

- **Python 3.10+** installed
- **Ollama** installed and running (`ollama serve`)
- **Llama 3.1** model pulled (`ollama pull llama3.1`)
- **NVIDIA GPU** (Recommended: RTX 3060 or better) with CUDA support
  - CPU mode is supported but significantly slower

### Installing Ollama

1. Download Ollama from [ollama.ai](https://ollama.ai)
2. Install and start the service:
   ```bash
   ollama serve
   ```
3. Pull the required model:
   ```bash
   ollama pull llama3.1
   ```

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd wikipedia-speedrun
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```
   
   **Windows:**
   ```bash
   .\venv\Scripts\activate
   ```
   
   **Linux/Mac:**
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install PyTorch with CUDA support (if using GPU):**
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
   ```
   
   *Note: The requirements.txt includes torch, but for CUDA support, you may need to install it separately as shown above.*

## 🚀 Usage

### Running the Comparison

Run the main comparison script to see all three methods compete:

```bash
python comparison.py
```

This will:
- Test all three methods on predefined scenarios
- Display real-time progress for each method
- Show a comparison table at the end with results

### Example Output

```
🏆 WIKIPEDIA SPEEDRUN ALGORITHM BATTLE 🏆
============================================================

🌍 SCENARIO: Potato -> Barack Obama
------------------------------------------------------------
▶️  AGENT: Hybrid (Method 1) Running...
      📍 Start: [Potato]
      👉 [Step 1] Potato --> 'Agriculture'
      👉 [Step 2] Agriculture --> 'United States'
      ...
🏁 RESULT: SUCCESS! (45.23 seconds)
```

### Custom Scenarios

To test your own scenarios, edit `comparison.py` and modify the `SCENARIOS` list:

```python
SCENARIOS = [
    {
        "start": "https://en.wikipedia.org/wiki/YourStartPage",
        "target": "Your Target Topic",
        "keywords": "target keywords for semantic search"
    },
]
```

## 📁 Project Structure

```
wikipedia-speedrun/
├── comparison.py      # Main comparison script that runs all methods
├── method_1.py        # Hybrid Standard approach (SBERT + LLM)
├── method_2.py        # Pure SBERT approach (vector similarity only)
├── method_3.py        # Chain-of-Thought approach (reasoning + LLM)
├── utils.py           # Shared utilities (link extraction, SBERT matching)
├── requirements.txt   # Python dependencies
├── README.md          # This file
└── venv/              # Virtual environment (not in repo)
```

## 🔧 How It Works

1. **Link Extraction**: Fetches Wikipedia page, extracts valid article links, filters non-article pages
2. **Semantic Filtering**: Uses SBERT (`all-MiniLM-L6-v2`) to encode target keywords and link titles, calculates cosine similarity, returns top K matches
3. **Decision Making**: 
   - Method 1: LLM selects from top 10 SBERT matches
   - Method 2: Direct selection of top 1 SBERT match
   - Method 3: LLM reasons through top 5 matches with explanations
4. **Navigation**: Follows selected link, tracks visited pages, checks for shortcuts, stops on success/dead end/timeout (15 steps max)

## 🐛 Troubleshooting

**Ollama Issues:** Ensure `ollama serve` is running, check model with `ollama list`, verify PATH

**GPU Issues:** Verify CUDA: `python -c "import torch; print(torch.cuda.is_available())"`, reinstall PyTorch with CUDA support, check with `nvidia-smi`

**Slow Performance:** Ensure GPU usage, reduce `top_k` values, use Method 2 for speed, or try smaller LLM model

**Model Download:** Check internet (first run only), model caches after download, verify `sentence-transformers` installed

**Wikipedia Blocking:** Code includes User-Agent header, add delays if needed, consider Wikipedia API

## 📊 Performance Notes

- **Method 1 (Hybrid)**: Best balance of speed and accuracy
- **Method 2 (Pure SBERT)**: Fastest, good for simple connections
- **Method 3 (CoT)**: Slowest but most thorough for complex paths

Typical performance on RTX 3060:
- Method 1: 3-5 seconds per step
- Method 2: <1 second per step
- Method 3: 10-15 seconds per step

## 🧪 Test Results Analysis

Based on real test runs with 3 challenging scenarios:

### Overall Performance Summary

| Method | Success Rate | Avg Time | Avg Steps | Best For |
|--------|-------------|----------|-----------|----------|
| **Method 1 (Hybrid)** | **100% (3/3)** | **5.5s** | **5.3 steps** | **General use - most reliable** |
| Method 2 (SBERT) | 67% (2/3) | 6.1s | 10 steps | Simple, direct connections |
| Method 3 (CoT) | 100% (3/3) | 13.6s | 7 steps | Complex, indirect paths |

### Key Findings

✅ **Method 1 (Hybrid) - The Winner:**
- **100% success rate** across all scenarios
- Consistent performance (3-8 seconds)
- Efficient pathfinding (4-7 steps)
- Successfully avoided semantic traps that caught Method 2

⚠️ **Method 2 (SBERT) - Speed Demon with Risks:**
- Fastest when it works (2.5-9.5 seconds)
- **Failed on complex scenario** (Hallucinogenic fish → Andrej Karpathy)
- Got trapped by homonyms:
  - "White House at Night" (painting) instead of "White House" (building)
  - "Tesla" (film) instead of "Tesla" (company/scientist)
- Validates README warning: "Easily trapped by homonyms"

🤔 **Method 3 (CoT) - The Reliable Thinker:**
- **100% success rate** - never failed
- Slowest overall (5-29 seconds)
- Most thorough reasoning for complex paths
- Sometimes "overthinks" simple paths (took longer than Method 1 in Scenario 2)

### Real-World Example: Potato → Barack Obama

- **Method 1**: Potato → United States → African American → **Barack Obama** (4 steps, 7.6s)
- **Method 2**: Potato → Anton Mauve → White House at Night → ... (14 steps, 9.6s) - *Got distracted by "White House" painting*
- **Method 3**: Potato → United States → President → **Barack Obama** (4 steps, 5.3s) - *Most direct path*

### Conclusion

**Method 1 (Hybrid)** proves to be the optimal choice for general use, combining the speed of semantic search with the intelligence of LLM reasoning. It successfully avoids the pitfalls that trap pure vector-based approaches while maintaining reasonable speed.

---

<a id="türkçe-dokümantasyon"></a>
# 🇹🇷 Türkçe Dokümantasyon

## 🎯 Genel Bakış

Wikipedia Oyunu, rastgele bir Wikipedia makalesinden başlayıp sadece linklere tıklayarak hedef makaleye ulaşma oyunudur. Bu proje, bu süreci otomatikleştirir ve üç farklı AI destekli yaklaşımı karşılaştırır.

**Özellikler:**
- 🚀 Tamamen offline çalışma (API anahtarı gerekmez)
- 🧠 Semantik arama ve LLM akıl yürütmeyi birleştiren hibrit AI yaklaşımı
- ⚡ Farklı hız/doğruluk dengesi için çoklu algoritmalar
- 📊 Karşılaştırmalı performans analizi
- 🎮 Önceden yapılandırılmış zorlu senaryolar

## 🧠 Karşılaştırılan Metodolojiler

### 1. Hibrit Standart (Şampiyon 🏆)
**Dosya:** `method_1.py`

- **Mantık:** SBERT ile en yakın 10 linki bulur, sonra **Llama 3.1**'den en mantıklı olanı seçmesini ister
- **Artıları:** Hızlı (adım başına 3-5s), bağlam farkındalığı, semantik tuzaklardan kaçınır
- **Eksileri:** Saf vektör yaklaşımından biraz daha yavaş

### 2. Saf SBERT (Hız Canavarı ⚡)
**Dosya:** `method_2.py`

- **Mantık:** Hedef vektör ile link vektörleri arasındaki kosinüs benzerliğini hesaplar, en yakın linki anında seçer
- **Artıları:** Çok hızlı (adım başına <1s), LLM yükü yok
- **Eksileri:** Bağlam körü, homonimlerle kolayca tuzağa düşer

### 3. Düşünce Zinciri (Profesör 🤔)
**Dosya:** `method_3.py`

- **Mantık:** En iyi 5 linki filtreler, sonra Llama 3.1'den **akıl yürütmesini açıklamasını** ister
- **Artıları:** Karmaşık, dolaylı bağlantılar için en yüksek doğruluk potansiyeli
- **Eksileri:** Açıklamalar için token üretimi nedeniyle en yavaş, basit yolları "fazla düşünür"

## 🛠️ Gereksinimler

- **Python 3.10+** yüklü
- **Ollama** yüklü ve çalışıyor (`ollama serve`)
- **Llama 3.1** modeli indirilmiş (`ollama pull llama3.1`)
- **NVIDIA GPU** (Önerilen: RTX 3060 veya daha iyi) CUDA desteği ile
  - CPU modu desteklenir ancak çok daha yavaştır

### Ollama Kurulumu

1. [ollama.ai](https://ollama.ai) adresinden Ollama'yı indirin
2. Servisi başlatın:
   ```bash
   ollama serve
   ```
3. Gerekli modeli indirin:
   ```bash
   ollama pull llama3.1
   ```

## 📦 Kurulum

1. **Repository'yi klonlayın:**
   ```bash
   git clone <repository-url>
   cd wikipedia-speedrun
   ```

2. **Sanal ortam oluşturun:**
   ```bash
   python -m venv venv
   ```
   
   **Windows:**
   ```bash
   .\venv\Scripts\activate
   ```
   
   **Linux/Mac:**
   ```bash
   source venv/bin/activate
   ```

3. **Bağımlılıkları yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

4. **GPU için PyTorch CUDA desteği (opsiyonel):**
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
   ```

## 🚀 Kullanım

### Karşılaştırmayı Çalıştırma

Üç yöntemin rekabetini görmek için ana karşılaştırma scriptini çalıştırın:

```bash
python comparison.py
```

Bu script:
- Önceden tanımlanmış senaryolarda üç yöntemi test eder
- Her yöntem için gerçek zamanlı ilerlemeyi gösterir
- Sonunda sonuçlarla bir karşılaştırma tablosu gösterir

### Örnek Çıktı

```
🏆 WIKIPEDIA SPEEDRUN ALGORITHM BATTLE 🏆
============================================================

🌍 SCENARIO: Potato -> Barack Obama
------------------------------------------------------------
▶️  AGENT: Hybrid (Method 1) Running...
      📍 Start: [Potato]
      👉 [Step 1] Potato --> 'Agriculture'
      👉 [Step 2] Agriculture --> 'United States'
      ...
🏁 RESULT: SUCCESS! (45.23 seconds)
```

### Özel Senaryolar

Kendi senaryolarınızı test etmek için `comparison.py` dosyasını düzenleyin ve `SCENARIOS` listesini değiştirin:

```python
SCENARIOS = [
    {
        "start": "https://en.wikipedia.org/wiki/BaşlangıçSayfası",
        "target": "Hedef Konu",
        "keywords": "hedef anahtar kelimeler semantik arama için"
    },
]
```

## 📁 Proje Yapısı

```
wikipedia-speedrun/
├── comparison.py      # Tüm yöntemleri çalıştıran ana karşılaştırma scripti
├── method_1.py        # Hibrit Standart yaklaşım (SBERT + LLM)
├── method_2.py        # Saf SBERT yaklaşımı (sadece vektör benzerliği)
├── method_3.py        # Düşünce Zinciri yaklaşımı (akıl yürütme + LLM)
├── utils.py           # Ortak yardımcı fonksiyonlar (link çıkarma, SBERT eşleştirme)
├── requirements.txt   # Python bağımlılıkları
├── README.md          # Bu dosya
└── venv/              # Sanal ortam (repo'da değil)
```

## 🔧 Nasıl Çalışır

1. **Link Çıkarma**: Wikipedia sayfasını getirir, geçerli makale linklerini çıkarır, makale olmayan sayfaları filtreler
2. **Semantik Filtreleme**: SBERT (`all-MiniLM-L6-v2`) kullanarak hedef anahtar kelimeleri ve link başlıklarını kodlar, kosinüs benzerliği hesaplar, en iyi K eşleşmeyi döndürür
3. **Karar Verme**: 
   - Yöntem 1: LLM en iyi 10 SBERT eşleşmesinden seçer
   - Yöntem 2: En iyi 1 SBERT eşleşmesini doğrudan seçer
   - Yöntem 3: LLM en iyi 5 eşleşmeyi akıl yürüterek açıklamalarla seçer
4. **Navigasyon**: Seçilen linki takip eder, ziyaret edilen sayfaları takip eder, kısayolları kontrol eder, başarı/çıkmaz/zaman aşımında durur (maksimum 15 adım)

## 🐛 Sorun Giderme

**Ollama Sorunları:** `ollama serve` çalıştığından emin olun, modeli `ollama list` ile kontrol edin, PATH'i doğrulayın

**GPU Sorunları:** CUDA'yı doğrulayın: `python -c "import torch; print(torch.cuda.is_available())"`, PyTorch'u CUDA desteği ile yeniden yükleyin, `nvidia-smi` ile kontrol edin

**Yavaş Performans:** GPU kullanımını sağlayın, `top_k` değerlerini azaltın, hız için Yöntem 2'yi kullanın veya daha küçük LLM modeli deneyin

**Model İndirme:** İnternet bağlantısını kontrol edin (sadece ilk çalıştırmada), model indirmeden sonra önbelleğe alınır, `sentence-transformers` yüklü olduğunu doğrulayın

**Wikipedia Engelleme:** Kod User-Agent başlığı içerir, gerekirse gecikmeler ekleyin, Wikipedia API'sini düşünün

## 📊 Performans Notları

- **Yöntem 1 (Hibrit)**: Hız ve doğruluk dengesi en iyi
- **Yöntem 2 (Saf SBERT)**: En hızlı, basit bağlantılar için iyi
- **Yöntem 3 (Düşünce Zinciri)**: En yavaş ama karmaşık yollar için en kapsamlı

RTX 3060'ta tipik performans:
- Yöntem 1: Adım başına 3-5 saniye
- Yöntem 2: Adım başına <1 saniye
- Yöntem 3: Adım başına 10-15 saniye

## 🧪 Test Sonuçları Analizi

3 zorlu senaryo ile gerçek test sonuçlarına göre:

### Genel Performans Özeti

| Yöntem | Başarı Oranı | Ortalama Süre | Ortalama Adım | En İyi Kullanım |
|--------|-------------|---------------|---------------|-----------------|
| **Yöntem 1 (Hibrit)** | **%100 (3/3)** | **5.5s** | **5.3 adım** | **Genel kullanım - en güvenilir** |
| Yöntem 2 (SBERT) | %67 (2/3) | 6.1s | 10 adım | Basit, doğrudan bağlantılar |
| Yöntem 3 (Düşünce Zinciri) | %100 (3/3) | 13.6s | 7 adım | Karmaşık, dolaylı yollar |

### Önemli Bulgular

✅ **Yöntem 1 (Hibrit) - Kazanan:**
- Tüm senaryolarda **%100 başarı oranı**
- Tutarlı performans (3-8 saniye)
- Verimli yol bulma (4-7 adım)
- Yöntem 2'nin takıldığı semantik tuzaklardan başarıyla kaçındı

⚠️ **Yöntem 2 (SBERT) - Hız Canavarı ama Riskli:**
- Çalıştığında en hızlı (2.5-9.5 saniye)
- **Karmaşık senaryoda başarısız** (Hallucinogenic fish → Andrej Karpathy)
- Homonimlerle tuzağa düştü:
  - "White House at Night" (resim) yerine "White House" (bina)
  - "Tesla" (film) yerine "Tesla" (şirket/bilim insanı)
- README uyarısını doğruladı: "Homonimlerle kolayca tuzağa düşer"

🤔 **Yöntem 3 (Düşünce Zinciri) - Güvenilir Düşünür:**
- **%100 başarı oranı** - hiç başarısız olmadı
- En yavaş genel performans (5-29 saniye)
- Karmaşık yollar için en kapsamlı akıl yürütme
- Bazen basit yolları "fazla düşünür" (Senaryo 2'de Yöntem 1'den daha uzun sürdü)

### Gerçek Dünya Örneği: Potato → Barack Obama

- **Yöntem 1**: Potato → United States → African American → **Barack Obama** (4 adım, 7.6s)
- **Yöntem 2**: Potato → Anton Mauve → White House at Night → ... (14 adım, 9.6s) - *"White House" resmiyle dikkati dağıldı*
- **Yöntem 3**: Potato → United States → President → **Barack Obama** (4 adım, 5.3s) - *En doğrudan yol*

### Sonuç

**Yöntem 1 (Hibrit)** genel kullanım için optimal seçim olduğunu kanıtladı. Semantik aramanın hızını LLM akıl yürütmesinin zekasıyla birleştiriyor. Saf vektör tabanlı yaklaşımların tuzağına düşmeden makul bir hız koruyor.

## 📚 Referanslar

- [Sentence-BERT](https://www.sbert.net/)
- [Ollama](https://ollama.ai/)
- [Wikipedia Game](https://en.wikipedia.org/wiki/Wikipedia:Wiki_Game)

**İyi Speedrun'lar! 🏎️💨**
