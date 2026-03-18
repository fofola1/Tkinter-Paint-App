## Aplikace musí běžet bez chyb
- ošetřit hranice rastru
- ošetřit vykreslování VŠEMI SMĚRY (zkuste i úplně svyslou čáru)

## Další funkce

Před přidíním čáry vidím "náhled" (před potvrzením druhého bodu se bude vykreslovat čára mezi prvním bodem a kurzorem)

implementovat tečkované čáry pokud je stisknuta klávesa Control
- pro uložené úsečky
- pro náhled

po stisknutí klávesy C se vše smaže

Pokud je stisknuta klávesa Shift, pak se čára vykreslí zarovnaná (vodorovná/svislá/45°/-45°)

## Polygon

Přidat obládací prvky pro změnu módu (aktuálně pro polygon, časem pro další objekty)

polygon se vyhreslí po zadání minimálně 3 bodů.

pro polygon platí veškeré předešlé podmínky. (tečkované čáry - CTRL, zarovnání - Shift)

--- 

# Zadání kompletní

# Projekt

Tento projekt se zaměřuje na vytvoření aplikace pro kreslení základních geometrických prvků s důrazem na vlastní implementaci algoritmů.

> **Důležité upozornění:** Všechny implementované algoritmy musí být součástí vašeho zdrojového kódu. Není povoleno využívat knihovny třetích stran pro logiku vykreslování!

> Pokud vámi vybraná technologie neumožňuje splnit jakýkoliv z bodů zadání, prosím o konzultaci zda je daná technologie vhodná pro tento projekt.

---

## Cíl projektu
Cílem projektu je vytvořit jednoduchý kreslící program podobný aplikaci Malování ve Windows, ale s jednodušší funkcionalitou. Program bude umožňovat kreslení základních tvarů, jejich následnou úpravu a mazání.

---

## Funkce aplikace

### 1. Kreslení čar
- [x] **Parametry:** Volba barvy, tloušťky a stylu čáry.
- [x] **Styly:** Plná, přerušovaná, tečkovaná.

### 2. Základní tvary
Možnost vykreslování následujících objektů:
- [x] Kružnice
- [x] Čtverec
- [x] Obdélník
- [x] Libovolný polygon

### 3. Úpravy tvarů
- [x] **Změna rozměrů:** Úprava velikosti a tvaru tažením myší.
- [x] **Manipulace:** Přesouvání objektů po ploše plátna.

### 4. Další nástroje
- [x] **Guma:** Nástroj pro mazání obsahu.
- [x] **Výplň:** Možnost vyplnění uzavřených objektů a oblastí barvou.
- [ ] **Delete:** Vymazání celého plátna.

### 5. Uživatelské rozhraní (UI)
- [x] Barevná paleta pro výběr odstínů.
- [x] Ovládací prvky pro nastavení tloušťky a typu čáry.
- [x] Přehledné menu pro výběr nástrojů a tvarů.

---

## Očekávané výstupy
* **Aplikace:** Plně funkční program splňující výše uvedené body.
* **Zdrojový kód:** Komentovaný kód bez závislostí na externích grafických knihovnách.
* **Dokumentace:** Stručný technický popis a uživatelský návod k použití.

### Jakákoliv rozšiřující funkčnost je vítána.