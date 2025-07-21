

import time, pathlib, random
import importlib
import subprocess
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.segment import Segment

console = Console()

# Előfeltételek biztosítása
REQUIRED_PACKAGES = ['pyperclip', 'undetected-chromedriver', 'selenium']
def auto_install_and_import(package):
    try:
        importlib.import_module(package)
    except ImportError:
        print(f"⚠️  {package} nincs telepítve. Telepítés próbálkozik...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        console.clear()
        header = Text("🔎 Anti-Bot-Detection //undetected-chromedriver// telepítése sikeres! 🔐")
        header.stylize("bold green")
        console.print(Align.center(header))
        console.print()

for pkg in REQUIRED_PACKAGES:
    auto_install_and_import(pkg)

from datetime import datetime
import json
import pyperclip
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import importlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).parent.resolve()
COMPONENTS_DIR = ROOT / "src/components/"
OUTPUT_DIR = ROOT / "generated_docs"
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

def load_config():
    config_file = ROOT / "config.json"
    with open(config_file, encoding="utf-8") as f:
        return json.load(f)

CONFIG = load_config()
BOT_MENTION = "@frontend_docs_generator"
INPUT_SELECTORS = CONFIG.get("merlin_input_selectors", [
    "div[contenteditable='true'][role='textbox']",
    "div[contenteditable='true'].tiptap",
    "div.tiptap.ProseMirror[contenteditable='true']",
    "textarea[placeholder*='Ask']",
    "textarea[placeholder*='Type']",
    "[data-testid='chat-input']",
    "input.relative.z-50.h-full.w-full.rounded-full",
    "input[type='text'][class*='rounded-full']"
])
RESPONSE_SELECTORS = CONFIG.get("merlin_response_selectors", [
    "div.flex.flex-col.items-start.whitespace-pre-wrap.break-words", 
    "div.message-content"
])
COPY_BUTTON_SELECTOR = CONFIG.get("merlin_copy_button_selector", ["svg.lucide-copy"])[0]
WAIT_TIMEOUT = CONFIG.get("wait_timeout", 90)
SITE_URL = CONFIG.get("merlin_site_url", "https://www.getmerlin.in/hu/chat")
HEADLESS = CONFIG.get("headless", False)

class HumanBehavior:
    @staticmethod
    def realistic_delay(min_sec=1.0, max_sec=3.0):
        delay = random.uniform(min_sec, max_sec)
        if random.random() < 0.3:
            delay += random.uniform(0.5, 2.0)
        time.sleep(delay)
    @staticmethod
    def human_mouse_movement(driver, element=None):
        try:
            action = ActionChains(driver)
            if element:
                action.move_to_element_with_offset(element, random.randint(-20, 20), random.randint(-20, 20))
                action.move_to_element(element)
            else:
                body = driver.find_element(By.TAG_NAME, "body")
                action.move_to_element_with_offset(body, random.randint(100, 800), random.randint(100, 600))
            action.pause(random.uniform(0.1, 0.5))
            action.perform()
        except:
            pass
    @staticmethod
    def scroll_like_human(driver):
        try:
            scroll_amount = random.randint(100, 500)
            direction = random.choice([1, -1])
            driver.execute_script(f"window.scrollBy(0, {scroll_amount * direction});")
            time.sleep(random.uniform(0.5, 1.5))
            if random.random() < 0.3:
                time.sleep(random.uniform(0.2, 0.8))
                driver.execute_script(f"window.scrollBy(0, {-scroll_amount//2});")
        except:
            pass

def clean_vue_code(code: str) -> str:
    lines = []
    for line in code.split('\n'):
        cleaned_line = line.rstrip()
        if cleaned_line.strip():
            lines.append(cleaned_line)
    cleaned_code = '\n'.join(lines)
    while '\n\n\n' in cleaned_code:
        cleaned_code = cleaned_code.replace('\n\n\n', '\n\n')
    return cleaned_code.strip()

def build_vue_message(component_path: pathlib.Path) -> str:
    raw_code = component_path.read_text(encoding="utf-8")
    cleaned_code = clean_vue_code(raw_code)
    console.print(f"\t🧹 [white] Vue fájl whitespace-mentesítése folyamatban[/white]")
    console.print(f"\t📝 [green]Eredeti fájl hossza[/green]: [gray]{len(raw_code)} karakter[/gray]")
    console.print(f"\t✍🏻 [bold green]Tisztított fájl hossza:[/bold green] [bold white]{len(cleaned_code)} karakter[/bold white]")
    return cleaned_code

def create_undetectable_browser():
    options = uc.ChromeOptions()
    if HEADLESS:
        options.headless = True
    options.add_argument("--window-size=1366,768")
    if "chrome_user_data_dir" in CONFIG:
        options.add_argument(f"--user-data-dir={CONFIG['chrome_user_data_dir']}")
    return uc.Chrome(options=options)

def find_textbox_safely(driver, wait, retries=8):
    for attempt in range(retries):
        print(f"🔍 Textbox keresés... (kísérlet {attempt + 1}/{retries})")
        HumanBehavior.scroll_like_human(driver)
        HumanBehavior.human_mouse_movement(driver)
        for selector in INPUT_SELECTORS:
            try:
                textbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                print(f"✅ Textbox megtalálva: {selector}")
                return textbox
            except:
                continue
        if attempt < retries - 1:
            print("🔄 Textbox nem található, újrapróbálkozás...")
            HumanBehavior.realistic_delay(2, 5)
    print("❌ Textbox nem található egyetlen selectorral sem!")
    return None

def paste_and_verify(driver, textbox, text, max_attempts=5):
    for attempt in range(1, max_attempts + 1):
        pyperclip.copy(text)
        time.sleep(0.1)
        textbox.click()
        driver.execute_script("arguments[0].focus();", textbox)
        time.sleep(0.2)
        textbox.send_keys(Keys.CONTROL, 'a')
        time.sleep(0.07)
        textbox.send_keys(Keys.BACKSPACE)
        time.sleep(0.07)
        textbox.send_keys(Keys.CONTROL, 'v')
        time.sleep(0.25)
        content = driver.execute_script("return arguments[0].innerText;", textbox).strip()
        print(f"👁️ ({attempt}) Szöveg a mezőben: {content!r}")
        HumanBehavior.realistic_delay(0.08,0.16)
        # Nincs whitespace, nincs torzulás, nincs HTML-link, csak a pontos szöveg
        if content == text:
            print("✅ Beillesztés OK, nincs torzulás")
            return True
        else:
            print("❗ Torzulás vagy extra elem (char count:", len(content), "), újrapróba...")
            if attempt == max_attempts:
                raise Exception(f"[FATAL] {max_attempts} próba után sem pontos a beillesztés: '{content}'")
    return False

def send_vue_code_like_human(driver, wait, vue_code, max_mention_attempts=5):
    textbox = find_textbox_safely(driver, wait)
    if not textbox:
        print("🚨 Nem található mező, aborting.")
        return False
    for attempt in range(max_mention_attempts):
        try:
            paste_and_verify(driver, textbox, BOT_MENTION)
            HumanBehavior.realistic_delay(0.45, 0.85)
            textbox.send_keys(Keys.ENTER)
            print("✅ @frontend_docs_generator elküldve enterrel.")
            break
        except Exception as e:
            print(f"↩️ Hiba beillesztésnél ({e}), újrapróba...")
            time.sleep(0.7)
    HumanBehavior.realistic_delay(1.2, 2.2)
    send_step_ok = False
    for step in range(1, 6):
        try:
            pyperclip.copy(vue_code)
            HumanBehavior.realistic_delay(0.19, 0.29)
            textbox = find_textbox_safely(driver, wait) 
            textbox.click()
            driver.execute_script("arguments[0].focus();", textbox)
            time.sleep(0.15)
            textbox.send_keys(Keys.CONTROL, 'a')
            time.sleep(0.07)
            textbox.send_keys(Keys.CONTROL, 'v')
            time.sleep(0.2)
            content = driver.execute_script("return arguments[0].innerText;", textbox).strip()
            if content.replace('\r','').replace('\n','').replace(' ','') == vue_code.replace('\r','').replace('\n','').replace(' ',''):
                print("✅ Vue kód pontosan a mezőben (karakterszám):", len(content))
                textbox.send_keys(Keys.ENTER)
                send_step_ok = True
                break
            else:
                print(f"❗ '{content[:20]}...' != '{vue_code[:20]}...', újrapróba")
                time.sleep(0.18)
        except Exception as e:
            print(f"[SEND VUE ERROR]: {e} — újrapróbál...")
            time.sleep(0.25)
    if not send_step_ok:
        print("❌ Nem sikerült helyesen elküldeni a vue kódot.")
        return False
    print("✅ Kód elküldve és enterrel jóváhagyva!")
    return True

def get_bot_markdown_response(driver, wait, copy_selector, fallback_selectors, timeout=90):
    for _ in range(timeout):
        time.sleep(1)
        try:
            copy_icons = driver.find_elements(By.CSS_SELECTOR, copy_selector)
            if copy_icons:
                HumanBehavior.human_mouse_movement(driver, copy_icons[-1])
                copy_icons[-1].click()
                time.sleep(0.5)
                response = pyperclip.paste()
                if response and response.strip():
                    print("✅ Markdown válasz vágólapról kimásolva!")
                    return response
        except Exception as e:
            pass
    print("⚠️ Copy ikon nem volt elérhető. Fallback textbox extract...")
    try:
        for selector in fallback_selectors:
            elems = driver.find_elements(By.CSS_SELECTOR, selector)
            if elems:
                print("✅ Fallback szövegelérés:", selector)
                return elems[-1].text
    except Exception as e:
        print("❌ Fallback extract hiba:", e)
    return None

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def save_markdown(content: str, title: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d-%H-%M")
    fname = OUTPUT_DIR / f"{title}_{ts}.md"
    
    # Teljes tartalom tisztítás
    content = clean_markdown_content(content)
    
    # Biztonságos mentés
    with open(fname, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    
    print(f"✅ Markdown mentve: {fname.relative_to(ROOT)}")
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def clean_markdown_content(content: str) -> str:
    import re
    content = content.replace('\r\n', '\n').replace('\r', '\n')

    # 2. Spec kar. javítás
    content = content.replace('\u00A0', ' ') 
    content = content.replace('\u2013', '-') 
    content = content.replace('\u2014', '--')
    content = content.replace('\u201C', '"') 
    content = content.replace('\u201D', '"') 
    
    # 3. Táblázat formáz. javítás
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        if '|' in line and line.strip() and not line.strip().startswith('#'):
            # Táblázat sor normalizálás
            parts = [part.strip() for part in line.split('|')]
            if len(parts) > 2:  # "tényleges" táblázat sor
                # Üres elemek eltávolítása elejéről és végéről
                while parts and not parts[0]:
                    parts.pop(0)
                while parts and not parts[-1]:
                    parts.pop()
                
                if parts:
                    fixed_line = '| ' + ' | '.join(parts) + ' |'
                    fixed_lines.append(fixed_line)
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        else:
            # Sorvégi whitespace eltávolítás
            fixed_lines.append(line.rstrip())
    
    content = '\n'.join(fixed_lines)
    
    # 4. Többszörös üres sorok korlátozása!!!
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    
    # 5. Fájl eleje/vége tisztítás
    content = content.strip() + '\n'
    
    return content

def run(component_files):
    driver = create_undetectable_browser()
    wait = WebDriverWait(driver, WAIT_TIMEOUT)
    try:
        console.print(f"[bold blue]🌐 Merlin oldal betöltése:[/bold blue][bold white]{SITE_URL}[/bold white]\n")
        driver.get(SITE_URL)
        
        panel_text = "Dokumentáció készítése folyamatban..."
        panel = Panel(panel_text, style="cyan", border_style="bright_cyan", padding=(1,2), expand=False)
        console.print(panel, justify="start", style="bold")
        
        HumanBehavior.scroll_like_human(driver)
        HumanBehavior.realistic_delay(1, 2)
        
        msg = Text()
        msg.append("Jelentkezzen be a regisztrált fiókjába!\n", style="bold yellow")
        msg.append("(Ahol a dokumntációt generáló ", style="white")
        msg.append("@bot", style="bold cyan italic")
        msg.append(" létre lett hozva.)\n", style="white")
        msg.append("(Amennyiben még nincsen létrehozva", style="white italic")
        msg.append(" ❯❯❯❯", style="yellow")
        msg.append(" README.MD ", style="bold cyan italic")
        msg.append("❮❮❮❮ ",style="yellow")
        msg.append("fájlban megtalálja!)", style="white italic")
        msg.justify = "center"
        login_info = Panel(
            msg,
            padding=(1, 2),
            expand=False,
            border_style="yellow"

        )
        console.print(Align.center(login_info))


        msg = Text()
        msg.append("Folytatáshoz\n", style="bold green underline")
        msg.append("Nyomja meg az ❯❯❯❯ ", style="bold white")
        msg.append("ENTER", style="bold green")
        msg.append(" ❮❮❮❮ billentyűt!\n\n", style="bold white")
        msg.append("Kilépéshez\n", style="bold red underline")
        msg.append("Nyomja meg a ❯❯❯❯", style="bold white")
        msg.append(" Ctrl + C ", style="bold red")
        msg.append("❮❮❮❮ billentyűt!", style="bold white")
        msg.justify = "center"

        enter_prompt = Panel(
        msg,
        border_style="bright_white",
        padding=(1, 2),
        expand=False)
        
        console.print(Align.center(enter_prompt))
        
        try:
            input()
            msg = Text()
            msg.append("🚀 Folytatás...", style="bold green")
            msg.justify='center'
            enter_continue=Panel(
                msg,
                padding=(1, 2)
            )
            console.print(Align.center(enter_continue))   
                     
        except KeyboardInterrupt:
            msg = Text()
            msg.append("❌ Megszakítva!", style="bold, red")
            msg.justify='center'
            ctrlc_exit=Panel(
                msg,
                padding=(1, 2)
            )
            console.print(Align.center(ctrlc_exit))   
            return
        
        HumanBehavior.scroll_like_human(driver)
        for idx, comp in enumerate(component_files, 1):
            console.print(f"\n\t[{idx}/{len(component_files)}][bold white] 📥 Fájl/fájlok kiválasztása:[bold white]")
            vue_mini = "[bold green] ▼ [/bold green]"  
            console.print(f"\n\t{vue_mini} [bright_green]{comp.name}[/bright_green]")
            vue_code = build_vue_message(comp)
            HumanBehavior.realistic_delay(1.8, 3.0)
            mention_and_code_ok = send_vue_code_like_human(driver, wait, vue_code)
            if not mention_and_code_ok:
                print("❌ Nem sikerült bemenetet beadni ebben a körben!")
                continue
            print("⏳ Várakozás a bot válaszára (átlag 15-35 másodperc)...")
            wait_time = random.randint(15,35)
            for _ in range(wait_time // 20):
                time.sleep(20)
                HumanBehavior.scroll_like_human(driver)
            time.sleep(wait_time % 20)
            markdown = get_bot_markdown_response(driver, wait, COPY_BUTTON_SELECTOR, RESPONSE_SELECTORS)
            if markdown and markdown.strip():
                save_markdown(markdown, comp.stem)
                print(f"\n✅ Fájl ok: {comp.name}")
            else:
                print(f"\n❌ NEM sikerült markdown választ menteni: {comp.name}")
        HumanBehavior.realistic_delay(3, 6)
    except Exception as e:
        print(f"‼️ Általános hiba: {e}")
    finally:
        HumanBehavior.realistic_delay(2, 5)
        
        # Egyenlőre maradjon csak nyitva!
        # driver.quit()
        # print("✅ Böngésző bezárva.")

if __name__ == "__main__":
    robot_text = Text("🤖 🤖 🤖 Anti-Bot-Detection Bekapcsolva 🤖 🤖 🤖")
    robot_text.stylize("bold magenta")
    console.print(Align.center(robot_text))
    console.print()
    
    if len(sys.argv) > 1:
        vue_files = [pathlib.Path(p) for p in sys.argv[1:]]
    else:
        vue_files = list(COMPONENTS_DIR.glob("*.vue"))
    if not vue_files:
        print("Nincs .vue fájl!")
        sys.exit(1)
    file_info = Text("📁 Feldolgozandó [*.Vue] fájl(ok) száma: ", style="yellow")
    file_info.append(str(len(vue_files))+" db.", style="bold white")
    console.print(Align.center(file_info))
    console.print()
    run(vue_files)