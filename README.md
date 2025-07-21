# 🪄 *Vue-ból Merlin* Dokumentáció Generátor

Python alapú, **félautomata** rendszer, amely a [GetMerlin.in](https://www.getmerlin.in/) AI webes platformot használja arra, hogy Vue komponensekből (vagy más projektfájlokból) **automatikusan** **strukturált MarkDown** dokumentációt készítsen – **egyetlen paranccsal!**

## ✨ Fő funkciók

- 📝 **Automatikus dokumentáció generálás** Vue komponens(ek)ből
- 🌐 **Selenium + Chrome + Merlin webapp** összehangolt használata  
- ✅ **Headless mód támogatás** (láthatatlan böngészés)
- 📂 **Tömeges (batch) feldolgozás** – egész mappát is feldolgoz
- 🗂️ **Testreszabható output** (kimeneti mappa, prompt sablon)
- 🧠 **Emberi viselkedés szimulálás** (késleltetések, egérmozgás)
- 🛡️ **Részletes hibaüzenetek és magyar nyelvű workflow**
- 📋 **Automatikus vágólap kezelés** a válaszok kinyeréséhez

## 🛠️ Telepítési és elindítási útmutató

### 1. Python és Chrome/Chromedriver

- Python 3.9+ szükséges
- Chrome böngésző telepítve kell legyen
- [GetMerlin.in](https://www.getmerlin.in/) weboldalon **regisztrálj és jelentkezz be**

### 2. Projekt letöltése

```bash
git clone https://github.com/yourusername/vue-merlin-docs-generator
cd vue-merlin-docs-generator
```

### 3. Csomagok telepítése - ⚠️ Előfeltétel ⚠️

```bash
pip install pyperclip undetected-chromedriver selenium
```

### 4. Projekt struktúra

```
vue-merlin-docs-generator/
├── vue_docs_generator.py       # Fő szkript
├── config.json                 # Konfigurációs beállítások
├── README.md                   # Telepítési és használati útmutató
├── docs_generated/             # Generált dokumentációk
└── src/
    └── components/
        └── example.vue         # Vue komponensek
```

### 5. Chrome bejelentkezés tesztelése

- Chrome-ban nyisd meg a [GetMerlin.in](https://www.getmerlin.in/hu/chat) oldalt
- Jelentkezz be a fiókodba
- Ha látod a chat felületet, **minden OK!**

## ⚡ Használat – gyorsindítás

### 1. Egy *adott* komponens dokumentálása

```bash
python vue_docs_generator.py src/components/MyComponent.vue
```

### 2. Több komponens egyszerre

```bash
python vue_docs_generator.py src/components/Component1.vue src/components/Component2.vue
```

### 3. Teljes mappa feldolgozása

```bash
python vue_docs_generator.py src/components/
```

---

## ⚙️ Konfiguráció

A `config.json` fájl segítségével minden fontos opció állítható:

```json
{
  "merlin_input_selectors": [
    "div[contenteditable='true'][role='textbox']",
    "div[contenteditable='true'].tiptap",
    "div.tiptap.ProseMirror[contenteditable='true']",
    "textarea[placeholder*='Ask']",
    "textarea[placeholder*='Type']",
    "[data-testid='chat-input']",
    "input.relative.z-50.h-full.w-full.rounded-full",
    "input[type='text'][class*='rounded-full']"
  ],
  "merlin_response_selectors": [
    "div.flex.flex-col.items-start.whitespace-pre-wrap.break-words", 
    "div.message-content"
  ],
  "merlin_copy_button_selector": "svg.lucide-copy",
  "wait_timeout": 90,
  "merlin_site_url": "https://www.getmerlin.in/hu/chat",
  "headless": false,
  "chrome_user_data_dir": "C:/Users/YourUser/AppData/Local/Google/Chrome/User Data"
}
```

### Főbb konfigurációs opciók:

- **headless**: Fut-e láthatatlan böngészőben *(true/false)*
- **wait_timeout**: Másodperc, ameddig keres egy elemet
- **merlin_site_url**: A Merlin chat oldal URL-je
- **chrome_user_data_dir**: Chrome felhasználói profil elérési útja
- **merlin_input_selectors**: CSS selectorok a beviteli mezőhöz
- **merlin_response_selectors**: CSS selectorok a válasz kinyeréséhez

---

## 💡 Hibák, tippek

- **Nem ír be semmit a Chrome-ban vagy nem található a mező?**
    - Ellenőrizd, hogy be vagy-e jelentkezve a Merlin weboldalon
    - Próbálj meg manuálisan egy üzenetet írni a chat-ben

- **Nem generálódik dokumentáció, hibát dob?**
    - Ellenőrizd, hogy elérhető-e a Vue komponens és van tartalom benne
    - Nézd meg a Chrome DevTools Console-t (F12) hibákért

- **Slow/timeout/hosszú várakozás?**
    - Állíts nagyobb timeout értéket a `config.json`-ban
    - Ellenőrizd az internetkapcsolatot

- **A vágólapról nem tudja kinyerni a választ?**
    - Próbáld meg manuálisan a másolás gombot megnyomni
    - A szkript fallback módban megpróbálja közvetlenül kinyerni

---

## 📚 GYIK – gyakori kérdések

**1. Tényleg a Merlin weboldalát használja?**

Igen! Ezért is fontos, hogy már be legyél jelentkezve a Chrome-ban.

**2. Más nyelven is működik?**

A Merlin többnyelvű, de a szkript magyar nyelvű prompt-tal dolgozik alapértelmezetten.

**3. Egyedi prompt-okat is lehet?**

A szkript fix prompt-tal dolgozik, de könnyen módosítható a kódban.

**4. Biztonságos-e headless módban tesztelni?**

Igen! De először próbáld ki látható módban, hogy minden működik-e.

**5. Mit csinál pontosan az emberi viselkedés szimulálás?**

- Véletlenszerű késleltetéseket rak be
- Egérmozgást szimulál
- Realisztikus gépelési tempót alkalmaz

## 🧩 Részletes működés

### Fő osztályok és függvények:

#### `HumanBehavior` osztály
- **`realistic_delay()`**: Véletlenszerű, emberi késleltetés
- **`human_mouse_movement()`**: Egérmozgás szimulálása
- **`scroll_like_human()`**: Természetes görgetés

#### Főbb függvények:
- **`load_config()`**: Config fájl betöltése
- **`clean_vue_code()`**: Vue kód tisztítása
- **`create_undetectable_browser()`**: Böngésző inicializálás
- **`find_textbox_safely()`**: Beviteli mező megkeresése
- **`send_vue_code_like_human()`**: Kód beküldése emberi módon
- **`get_bot_markdown_response()`**: Válasz kinyerése
- **`save_markdown()`**: Dokumentáció mentése

### Munkamenet folyamata:

1. **Konfiguráció betöltése** `config.json`-ból
2. **Vue fájlok beolvasása** és előkészítése
3. **Chrome böngésző indítása** (detektálás-mentes módban)
4. **Merlin oldal megnyitása**
5. **Manuális bejelentkezésre várás**
6. **Vue kódok beküldése** egyenként
7. **Válaszok kinyerése** és mentése
8. **Dokumentációk létrehozása** `.md` formátumban

---

## 🗂️ **Projektfájlok és Szerkezet**

```
vue-merlin-docs-generator/
├── vue_docs_generator.py        # Fő Python szkript, minden automatizálás itt történik
├── config.json                  # Konfigurációs beállítások, selectorok, timeoutok
├── README.md                    # Teljes telepítési és használati útmutató
└── docs_generated/              # Kimeneti dokumentációk (generált .md fájlok)
    └── (itt jönnek létre az outputok)
└── src/
    └── components/
        └── *.vue               # Bármely Vue fájl, amit dokumentálni szeretnél
```

---

## ⚙️ **Működés Lépésről Lépésre**

1. **Követelmények**
    - Python 3.9+
    - Chrome böngésző
    - GetMerlin.in fiók, bejelentkezve

2. **Telepítsd a csomagokat**
    
    ```bash
    pip install pyperclip undetected-chromedriver selenium
    ```

3. **Állítsd be a fájlokat**
    - Vue fájlok: `src/components/*.vue`
    - Config: `config.json` (alapból jó!)

4. **Komponens dokumentálása**
    ```bash
    python vue_docs_generator.py src/components/MyComponent.vue
    ```

5. **Kimeneti dokumentációk**
    - Minden fájlhoz külön .md fájl
    - Alapból `docs_generated/` könyvtárba
    - Időbélyeggel ellátott fájlnevek

---

## 🛠️ **Fő Funkciók Magyarázata**

- **vue_docs_generator.py:**
  Automatizálja a Chrome indítást, input mező kitöltést, válasz olvasást, fájl mentést.

- **config.json:**
  Speciális selectorok, timeout értékek, URL-ek, böngésző beállítások.

---

## 🚩 **Javaslatok első próbához**

1. **Teszteld először egy fájllal:**
    ```bash
    python vue_docs_generator.py src/components/TestComponent.vue
    ```
    - Nézd meg, sikerül-e inputot adni a Chrome-ban a Merlin-nek
    - Jött-e létre `docs_generated/TestComponent_YYYYMMDD_HHMMSS.md`

2. **Ha működik, próbáld több fájllal is!**
    ```bash
    python vue_docs_generator.py src/components/
    ```

3. **Siker esetén**:
    - Dokumentációid .md formátumban lesznek, készen a következő fejlesztési folyamathoz!

---

## 💡 **Utolsó tippek**

- A `config.json`-ban minden CSS selector testreszabható
- Fejlesztés közben használd a nem-headless módot, hogy lásd mi történik
- A vágólap kezelés automatikus, de manuálisan is ellenőrizhető
- A szkript robosztus: többször próbálkozik hiba esetén

---
## 🤝 Közösségi támogatás | Hibabejelentés
Ha elakadsz, nyugodtan írj issue-t a GitHub repóban vagy kérdezz közvetlenül tőlem!

---

## 🙏 Köszönet

*Köszönjük a [GetMerlin.in](https://www.getmerlin.in/) csapatának a kiváló AI platform szolgáltatását!*

---

**Ha végképp elakadsz, bármely lépésnél vagy kódrészletnél, csak írj – segítek! Jó munkát, sok sikerélményt kívánok a dokumentációgeneráláshoz!** 🚀