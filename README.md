## Popis

# Webová aplikace pro autoservis Mogy-tech

Tento projekt je vytvořen v jazyce Python pomocí mikroframeworku Flask. Slouží jako webová prezentace a zároveň jednoduchý správce obsahu pro autoservis.

## Obsahuje:

-   veřejné stránky (hlavní stránka, služby, ceník, náhradní díly),
-   kontaktní formulář s odesláním e-mailu zákazníkovi i správci,
-   přihlašovací formulář pro administrátora,
-   oddělenou administrační sekci,
-   ochranu proti CSRF útokům,
-   práci s databází přes SQLAlchemy.

---

## Použité technologie

-   **Python 3.12**
-   **Flask** – hlavní backend framework
-   **Flask-WTF** – pro formuláře a CSRF ochranu
-   **Flask-Login** – pro správu přihlášení
-   **Flask-Admin** – pro administraci dat
-   **MySQL + SQLAlchemy** – pro databázi
-   **Jinja2** – šablonovací jazyk pro HTML
-   **SMTP (smtplib)** – pro odesílání e-mailů z formulářů

---

## Jak spustit aplikaci

## Instalace

Pokud již máte projekt uložený na ploše, nemusíte ho klonovat. Klonování je nutné pouze v případě, že chcete stáhnout projekt z externího zdroje, například z GitHubu. Pokud již máte všechny soubory a složky na správném místě, stačí jen ověřit, že máte správně nastavené virtuální prostředí a nainstalované všechny závislosti.

### Klonování repozitáře

```sh
git clone https://github.com/ZuzanaMogyorosi/TOTOFUNGUJE.git
cd webKUprave - muze se menit podle toho v jake slozce je
```

## Nastavení proměnných prostředí

V kořenové složce musí být soubor `.env`, který obsahuje citlivé údaje jako hesla, e-mailové přihlašovací údaje a databázové připojení.

Tento soubor **není součástí repozitáře** – místo něj je k dispozici `.env_example`, který ukazuje, co musíš vyplnit.

Pokud vytváříš nový projekt podle tohoto repozitáře, proveď následující:

1. Zkopíruj `.env_example` a přejmenuj ho na `.env`
2. Vyplň své vlastní hodnoty

### Vytvořte a aktivujte virtuální prostředí

```sh
python3 -m venv venv
source venv/bin/activate
```

Pro jistotu zkontrolujte, že jste ve virtuálním prostředí příkazem:

```sh
which python
```

Výsledek by měl být:

```
/Users/zuzanamogyorosi/Desktop/uparavujWebNaGithubu/muzesupravovatwebnagithubu/venv/bin/python
```

### Nainstalujte závislosti

```sh
pip install -r requirements.txt
```

Pokud je potřeba, upgradujte pip:

```sh
pip install --upgrade pip
```

### Spusťte aplikaci

```sh
python run.py
```

Aplikace poběží na:
http://localhost:5000

Pokud je aplikace v jiné složce, může být potřeba jiný příkaz.

## Použití

Po spuštění aplikace přejděte na http://localhost:5000 ve vašem webovém prohlížeči.

## Struktura projektu

```
TOTOFUNGUJE/
├── run.py                   # Spouští Flask aplikaci
├── requirements.txt         # Seznam všech potřebných knihoven
├── README.md                # Tento soubor s dokumentací
├── .env                     # Nastavení citlivých údajů (hesla, e-maily)
├── .gitignore               # Soubory, které se neukládají do Gitu
├── app/
│   ├── __init__.py          # Spouštění, konfigurace a propojení modulů
│   ├── models.py            # Databázové modely (tabulky)
│   ├── main_views.py        # Veřejné stránky: domovská stránka, ceník, atd.
│   ├── admin_routes.py      # Administrátorské funkce a jejich routy
│   ├── auth.py              # Přihlašování, odhlašování, ochrana pomocí Flask-WTF
│   ├── email_utils.py       # Odesílání e-mailů z formuláře
│   ├── static/
│   │   ├── css/             # Styly pro vzhled webu
│   │   ├── image/           # Obrázky a loga
│   │   └── js/
│   │       └── script.js    # JavaScript pro validaci formulářů a funkce navigace
│   └── templates/           # HTML šablony pomocí Jinja2
│       ├── index.html       # Hlavní stránka
│       ├── login.html       # Přihlašovací formulář
│       ├── priceList.html   # Ceník
│       ├── services.html    # Služby
│       ├── spare_parts.html # Náhradní díly
│       └── thank_you.html   # Stránka po odeslání formuláře
└── venv/                    # Virtuální prostředí (lokální knihovny, neukládat do GitHubu)

```

Bezpečnostní prvky
Ochrana formulářů pomocí Flask-WTF a CSRF token v index.html formuláři a následné ošetření v souboru **init**.py

Hesla se porovnávají pomocí check_password_hash v souboru auth.py

Citlivé údaje jako hesla a e-maily nejsou v kódu – jsou uloženy v .env souboru

Admin sekce dostupná pouze po přihlášení - ta se nachází na hlavní stránce - index.html dole ve footeru v posledním sloupci.

Jak aplikace funguje
Spuštění
python run.py zavolá funkci create_app() z **init**.py a spustí web.

**init**.py propojí všechny části (moduly) aplikace a připraví prostředí.

Veřejná část
Návštěvník si prohlíží stránky jako /, /cenik, /nahradni-dily, /nase-sluzby.

Může vyplnit formulář, který pošle e-mail správci i potvrzení zákazníkovi.

Administrace
Admin se přihlásí pomocí /auth/login.

Po úspěšném přihlášení může přistupovat k administraci – např. měnit obsah, spravovat ceník.

Databáze
Modely jsou uloženy v models.py a pracuje se s nimi pomocí SQLAlchemy.

Data se při spuštění aplikace automaticky vytvoří pomocí db.create_all().

Poznámky pro vývoj a úpravy
HTML šablony využívají Jinja2 → obsah se doplňuje z Pythonu, v admin sekci měníme měsíční akci na index.html, ceník, a náhradní díly - inzeráty

V login.html a index.html jsou použity FlaskForm prvky (např. {{ form.username() }})

Všechny vizuální (barvy, rozmístění, fonty) upravíte v souborech static/css/

JavaScript pro formuláře je v static/js/script.js
