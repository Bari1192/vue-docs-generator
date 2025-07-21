# Automata dokumentumgenerátor bot gyors beállítása

## 🤖 **Bot létrehozási útmutató**

Mivel közvetlenül nem lehet létrehozni botot a [GetMerlin](https://www.getmerlin.in/hu/chat) weboldalán úgy, hogy publikusan bárki hozzáférjen, ezért íme a **gyors, de részletes lépéssor** amit manuálisan kell elvégezni ***~3 perc alatt***:

### **1. [GetMerlin](https://www.getmerlin.in/hu/chat) Bot létrehozása ⛯**

**Lépések:**
1. **Jelentkezz be** a [GetMerlin.in](https://www.getmerlin.in/hu/chat) oldalára
2. **Navigálj** a **More** 🎲 menüpontra - a baloldali menüsávban, majd kattints rá!
3. Válaszd ki a [Bots](https://www.getmerlin.in/hu/chat/bots) menüpontot - vagy **kattints ide:** [Merlin Bots create](https://www.getmerlin.in/hu/chat/bots)
4. Kattints a <span style="background-color:white;Border-radius:3px;padding:2px;color:black;font-weight:bold;">+ Create Bot</span> menüpontra.
5. **Hozz létre új botot** <span style="Border-radius:3px;padding:2px;color:lightgreen;font-weight:bold;">@frontend_docs_generator</span> néven - a ***Name*** attribútumba írva.
6. A <span style="padding:2px;color:red;font-weight:bold;">*</span>prompts részben található üres szövegdobozba pedig az alábbi **promptot** (utasítás-sort) másolja be:

```
Készíts **strukturált MarkDown dokumentációt** az alábbi Vue komponens alapján, **pontosan ebben a sorrendben és formátumban**:

# **Komponens neve - szerkezete:**

## **1. Komponens áttekintése**
- **Célja és funkciója** (1-2 mondatban)
- **Fő felhasználói interakciók** listája

## **2. Külső függőségek**
- **Importok, csomagok** (ha vannak)
- **Betűtípusok, CDN-ek** (ha vannak)

## **3. Strukturális elemek**
**Táblázat minden HTML/Vue elemről:**

| **Elem** | **Funkció, stílusjegyek** |
|----------|---------------------------|
| `<div>` | *automatikusan kitöltendő* |

## **4. Logika és interakciók**
- **Script setup tartalom** (ha van)
- **Eseménykezelés** (ha van)
- **Reaktív adatok** (ha van)

## **5. Stílus összefoglaló**
**Táblázat:**

| **Kategória** | **Részletek** |
|---------------|---------------|
| **Színek** | *Tailwind osztályok* |
| **Betűtípus** | *Használt font-ok* |
| **Reszponzivitás** | *Breakpointok* |
| **Effektek** | *Hover, transition* |

## **Kiegészítő elvárások:**
- **Konzisztencia**: Ugyanilyen szerkezetű dokumentációt generálj minden alkalommal
- **Tömörség**: Lényegre törő, de teljes körű leírás
- **Példák**: Konkrét Tailwind osztályokat, színkódokat említs
- **Hibakeresés**: Ha valamit nem értsz a kódból, jelezd külön bekezdésben
- **Csak magyarul írj**
- **Táblázatokat mindig töltsd ki**
- **Ha nincs tartalom → "Nincs" válasz**
- **Ne add vissza a forráskódot**

## **Komponens kódját a felhasználó írja be, adja meg:**
```

### **2. Config.json Konfigurálása**

**Chrome profil elérési út megtalálása:**

**Windows esetén:**
```bash
# Chrome profil útvonala általában:
C:\Users\[FELHASZNÁLÓNÉV]\AppData\Local\Google\Chrome\User Data
```

**Példa config.json beállítás**
- *A projekt könyvtára **tartalmazza!***
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
  "merlin_copy_button_selector": ["svg.lucide-copy"],
  "wait_timeout": 90,
  "merlin_site_url": "https://www.getmerlin.in/hu/chat",
  "headless": false,
  "chrome_user_data_dir": "C:/Users/[AZ_ÖN_FELHASZNÁLÓNEVE]/AppData/Local/Google/Chrome/User Data"
}
```

## 🔧 **Telepítési folyamat**

### **Előfeltételek:**
- **Python 3.9+** telepítve
- **Google Chrome** böngésző
- **GetMerlin.in fiók** regisztrálva és bejelentkezve

### **Telepítési lépések:**

**1. Függőségek telepítése:**
- <span style="Border-radius:3px;padding:2px;color:yellow;font-weight:bold;">Figyelem !!!</span> Az alábbi parancs kiadásának **elmulasztásával** a program működésében funkcióvesztési problémák léphetnek elő!
```bash
pip install pyperclip undetected-chromedriver selenium rich
```

**2. Projekt struktúra létrehozása:**
```
vue-merlin-docs-generator/
├── run_generator.py            # Ez a fő Python szkript
├── config.json                 # Konfigurációs fájl
├── src/
│   └── components/
│       └── *.vue              # Vue komponensek ide!
└── generated_docs/            # Kimeneti dokumentációk
```

**3. Vue komponensek elhelyezése:**
- Helyezze el Vue fájljait a `src/components/` mappába
- Vagy adja meg közvetlenül a fájl elérési útját

## 🚀 **Használati útmutató**

### **Futtatási parancsok:**

**Egy komponens dokumentálása:**
```bash
python vue_docs_generator.py src/components/MyComponent.vue
```

**Több komponens egyszerre:**
```bash
python vue_docs_generator.py src/components/Component1.vue src/components/Component2.vue
```

**Teljes mappa feldolgozása:**
```bash
python vue_docs_generator.py
```

### <span style="Border-radius:3px;padding:2px;color:orange;font-weight:bold;text-decoration:underline;">Fontos futtatási lépések:</span>

1. **Böngészők bezárása:** Minden Chrome böngészőt zárjon be futtatás előtt
2. **Automatikus bejelentkezés:** A szkript automatikusan próbál bejelentkezni a megadott Chrome profillal.
3. *Legelső futáskor érdemes manuálisan bejelentkezni*
4. **Manuális folytatás:** A szkript megáll és ENTER billentyű lenyomására vár a folytatáshoz.
5. **Automatikus feldolgozás:** Minden Vue komponenst egyenként dolgoz fel
6. A program minden egyes lépését nyomon lehet követni a **Terminálon** a VS Code-on belüli interaktív felületen.

## ⚙️ **Speciális funkciók**

### **Emberi viselkedés szimulálás:**
- **Véletlenszerű késleltetések** (1-3 másodperc)
- **Realisztikus egérmozgás** szimulálás
- **Természetes görgetési** minták
- **Bot-detektálás elkerülése**

### **Hibakezelés és robusztusság:**
- **Többszörös újrapróbálkozás** hiba esetén
- **Automatikus fallback** mechanizmusok
- **Részletes hibaüzenetek** magyar nyelven
- **Vágólap automatikus kezelése**

### **Kimenet formázás:**
- **Automatikus Markdown tisztítás**
- **Táblázat formázás javítás**
- **Időbélyegzett fájlnevek**
- **UTF-8 kódolás biztosítása**

## 🔍 **Hibaelhárítás**

### **Gyakori problémák:**

**1. Nem található textbox:**
- Ellenőrizze a bejelentkezést GetMerlin.in-re
- Frissítse a `merlin_input_selectors` listát config.json-ban

**2. Timeout hibák:**
- Növelje a `wait_timeout` értéket 120-ra
- Ellenőrizze az internetkapcsolatot

**3. Chrome profil problémák:**
- Zárja be minden Chrome böngészőt
- Ellenőrizze a `chrome_user_data_dir` elérési útját

**4. Vágólap hibák:**
- Manuálisan tesztelje a másolás gombot
- Fallback mód automatikusan aktiválódik

## 📊 **Várható kimenet**

A generált dokumentációk a `generated_docs/` mappában jelennek meg ezzel a formátummal:
- **Fájlnév:** `KomponensNev_2024-07-20-14-30.md`
- **Struktúra:** A bot promptban megadott formátum szerint
- **Nyelvezet:** Magyar
- **Formázás:** Tiszta Markdown táblázatokkal

## 💡 **Optimalizálási tippek**

- **Első futtatás:** Manuálisan bejelntkezést igényelhet. Utána automatikusan menteni a profilt a használathoz.
- **Tömeges feldolgozás:** Kapcsolja át `"headless": true`-ra
- **Lassú kapcsolat esetén:** Növelje a timeout értékeket
- **Egyedi selectorok:** CSS selectorokat módosíthatja a config.json-ban

Ez a rendszer hatékonyan automatizálja a Vue komponens dokumentáció készítést, emberi viselkedést szimulálva és robosztus hibakezeléssel.

><span style="Border-radius:3px;padding:2px;color:lightyellow;font-weight:bold;">Figyelem!</span>
>> Amennyiben nem rendelkezik **előfizetéssel** a generálások mennyiségi korlátai **limitáltak**! A *Prompt*-ok optimalizálják a generálás gyorsaságát, hatékonyságát és segítenek az AI @bot-ok számára az információ hatékony feldolgozásában.
>> Az program felhasználása engedélyköteles / forráskód származásának megjelölése **kötelező**!