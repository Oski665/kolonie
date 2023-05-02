import pygame
import random
import math

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna gry
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Wymiary mapy (liczba pól)
szerokosc_mapy = 20
wysokosc_mapy = 15
PROG_ODLEGLOSCI_ZASOB = 5
PROG_ODLEGLOSCI_MAGAZYN = 25



# Rozmiar pojedynczego pola na mapie (w pikselach)
rozmiar_pola = 40


# Kolory
BIALY = (255, 255, 255)
ZIELONY = (0, 255, 0)
ZOLTY = (255, 255, 0)
NIEBIESKI = (0, 0, 255)
CZERWONY = (255, 0, 0)
SZARY = (128, 128, 128)
BRAZOWY = (139, 69, 19)
CZARNY = (0, 0, 0)


mapa = [
    # ...
    "####################",
    "#      ##      ####",
    "#      ##      ####",
    "#    5 ##  6   ####",
    "#      ##      ####",
    "#      ##      ####",
    "####################"
]

punktacja = {"a": 0, "b": 0}


# Zasoby
zasoby = {
    "drewno": [],
    "kamien": []
}

# Generowanie zasobów
def generuj_zasoby():
    for _ in range(100):
        typ = random.choice(["drewno", "kamien"])
        x = random.randint(0, width)
        y = random.randint(0, height)
        zasoby[typ].append((x, y))


zasoby_zajete = set()


# Kolonie
kolonia_a = [{"start": (random.randint(0, width), random.randint(0, height)),
              "pozycja": (random.randint(0, width), random.randint(0, height)),
              "zasob": None,
              "cel": None,
              "przenoszone": None} for _ in range(10)]


kolonia_b = [{"start": (random.randint(0, width), random.randint(0, height)),
              "pozycja": (random.randint(0, width), random.randint(0, height)),
              "zasob": None,
              "cel": None,
              "przenoszone": None} for _ in range(10)]


def rysuj_mape():
    for y, wiersz in enumerate(mapa):
        for x, pole in enumerate(wiersz):
            if pole == "1":
                screen.fill(ZIELONY, (x * rozmiar_pola, y * rozmiar_pola, rozmiar_pola, rozmiar_pola))
            elif pole == "2":
                screen.fill(ZOLTY, (x * rozmiar_pola, y * rozmiar_pola, rozmiar_pola, rozmiar_pola))
            elif pole == "3":
                screen.fill(NIEBIESKI, (x * rozmiar_pola, y * rozmiar_pola, rozmiar_pola, rozmiar_pola))
            elif pole == "4":
                screen.fill(CZERWONY, (x * rozmiar_pola, y * rozmiar_pola, rozmiar_pola, rozmiar_pola))


# Rysowanie zasobów na mapie
def rysuj_zasoby():
    for drewno in zasoby["drewno"]:
        if drewno not in zasoby_zajete:
            pygame.draw.circle(screen, ZOLTY, drewno, 5)
    for kamien in zasoby["kamien"]:
        if kamien not in zasoby_zajete:
            pygame.draw.circle(screen, ZIELONY, kamien, 5)


# Rysowanie kolonii na mapie
def rysuj_kolonie():
    for osobnik_a in kolonia_a:
        if osobnik_a["pozycja"] is not None:
            pygame.draw.circle(screen, NIEBIESKI, osobnik_a["pozycja"], 5)
            if osobnik_a["przenoszone"] is not None:
                pygame.draw.circle(screen, ZIELONY, osobnik_a["przenoszone"]["wspolrzedne"], 5)
    for osobnik_b in kolonia_b:
        if osobnik_b["pozycja"] is not None:
            pygame.draw.circle(screen, CZERWONY, osobnik_b["pozycja"], 5)
            if osobnik_b["przenoszone"] is not None:
                pygame.draw.circle(screen, ZOLTY, osobnik_b["przenoszone"]["wspolrzedne"], 5)


def rysuj_magazyny():
    for y, wiersz in enumerate(mapa):
        for x, pole in enumerate(wiersz):
            if pole == "5":
                screen.fill(BRAZOWY, (x * rozmiar_pola, y * rozmiar_pola, 5 * rozmiar_pola, 5 * rozmiar_pola))
            elif pole == "6":
                screen.fill(SZARY, (x * rozmiar_pola, y * rozmiar_pola, 5 * rozmiar_pola, 5 * rozmiar_pola))


magazyny = [
    {"typ": "a", "ilosc": 0, "wspolrzedne": (2 * rozmiar_pola + 2 * rozmiar_pola // 2, 4 * rozmiar_pola + 2 * rozmiar_pola // 2)},
    {"typ": "b", "ilosc": 0, "wspolrzedne": (17 * rozmiar_pola + 2 * rozmiar_pola // 2, 4 * rozmiar_pola + 2 * rozmiar_pola // 2)}
]


def rysuj_punktacje():
    font = pygame.font.Font(None, 36)
    text_a = font.render(f"Kolonia A: {punktacja['a']}", True, (255, 0, 0))
    text_b = font.render(f"Kolonia B: {punktacja['b']}", True, (0, 0, 255))
    screen.blit(text_a, (10, 10))
    screen.blit(text_b, (10, 50))


def rysuj():
    screen.fill(BIALY)
    rysuj_mape()
    rysuj_magazyny()
    rysuj_zasoby()
    rysuj_kolonie()
    rysuj_punktacje()
    pygame.display.flip()


def czy_w_magazynie(pozycja, kolonia_typ):
    magazyn_polozenie = (2, 4) if kolonia_typ == "a" else (17, 4)
    magazyn_srodek = (magazyn_polozenie[0] + 2, magazyn_polozenie[1] + 2)
    return odleglosc(pozycja, magazyn_srodek) < rozmiar_pola


# Obliczanie odległości między dwoma punktami
def odleglosc(p1, p2):
    if p1 is None or p2 is None:
        return float('inf')
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)



# Znajdowanie najbliższego zasobu do danego osobnika
def znajdz_najblizszy_wolny_zasob(pozycja_osobnika, zasob_typ):
    najblizszy_zasob = None
    najkrotsza_odleglosc = float("inf")
    for zasob in zasoby[zasob_typ]:
        if zasob not in zasoby_zajete:
            d = odleglosc(pozycja_osobnika, zasob)
            if d < najkrotsza_odleglosc:
                najblizszy_zasob = zasob
                najkrotsza_odleglosc = d
    return najblizszy_zasob



def zbierz_zasob(osobnik, kolonia_typ, zasoby):
    zasob_typ = "drewno" if kolonia_typ == "a" else "kamien"
    ilosc_zasobow = len(zasoby.get(zasob_typ))
    if ilosc_zasobow > 0:
        pozycja_zasobu = zasoby[zasob_typ].pop()
        osobnik["przenoszone"] = {"typ": zasob_typ, "wspolrzedne": pozycja_zasobu}
        zasoby_zajete.discard(pozycja_zasobu)


def dodaj_do_magazynu(punktacja, zasob, magazyny):
    for magazyn in magazyny:
        if magazyn["typ"] == zasob["typ"]:
            magazyn["ilosc"] += 1
            punktacja += 1
            return punktacja, magazyn
    return punktacja, None


def wybierz_zasob(osobnik, kolonia_typ):
    zasob_typ = "drewno" if kolonia_typ == "a" else "kamien"
    najblizszy_zasob = znajdz_najblizszy_wolny_zasob(osobnik["pozycja"], zasob_typ)
    if najblizszy_zasob is not None:
        zasoby_zajete.add(najblizszy_zasob)
        return najblizszy_zasob
    return None


def przesun_osobnika(osobnik, cel):
    kierunek = (cel[0] - osobnik["pozycja"][0], cel[1] - osobnik["pozycja"][1])
    dlugosc_kierunku = odleglosc(osobnik["pozycja"], cel)

    if dlugosc_kierunku != 0:
        krok = (kierunek[0] / dlugosc_kierunku, kierunek[1] / dlugosc_kierunku)
        krok = (krok[0] * 2, krok[1] * 2)
        nowa_pozycja = (osobnik["pozycja"][0] + krok[0], osobnik["pozycja"][1] + krok[1])
        osobnik["pozycja"] = nowa_pozycja

        if odleglosc(osobnik["pozycja"], cel) <= PROG_ODLEGLOSCI_ZASOB and osobnik["zasob"] is None:
            osobnik["zasob"] = cel
            dostepne_zasoby.remove(cel)

            osobnik["cel"] = magazyn
        elif odleglosc(osobnik["pozycja"], cel) <= PROG_ODLEGLOSCI_MAGAZYN and osobnik["zasob"] is not None:
            magazyn["zasoby"] += 1
            osobnik["zasob"] = None

            najblizszy_zasob = znajdz_najblizszy(osobnik["pozycja"], dostepne_zasoby)
            if najblizszy_zasob is not None:
                osobnik["cel"] = najblizszy_zasob
            else:
                osobnik["cel"] = magazyn


def aktualizuj_pozycje_kolonii(punktacja, kolonia_a, kolonia_b, zasoby, magazyny):
    magazyn_a_srodek = (2 * rozmiar_pola + rozmiar_pola * 2.5, 4 * rozmiar_pola + rozmiar_pola * 2.5)
    magazyn_b_srodek = (17 * rozmiar_pola + rozmiar_pola * 2.5, 4 * rozmiar_pola + rozmiar_pola * 2.5)

    for kolonia, kolonia_typ, magazyn_srodek in [(kolonia_a, "a", magazyn_a_srodek),
                                                 (kolonia_b, "b", magazyn_b_srodek)]:
        for osobnik in kolonia:
            if osobnik["cel"] is None:
                if osobnik["przenoszone"] is None:
                    osobnik["cel"] = wybierz_zasob(osobnik, kolonia_typ)
                else:
                    osobnik["cel"] = magazyn_srodek
            elif osobnik["przenoszone"] is None and odleglosc(osobnik["pozycja"],
                                                              osobnik["cel"]) < PROG_ODLEGLOSCI_ZASOB:
                zbierz_zasob(osobnik, kolonia_typ, zasoby)
            elif osobnik["przenoszone"] is not None and czy_w_magazynie(osobnik["pozycja"], kolonia_typ):
                punktacja[kolonia_typ], magazyn = dodaj_do_magazynu(punktacja[kolonia_typ], osobnik["przenoszone"],
                                                                    magazyny)
                zasoby_zajete.discard(osobnik["przenoszone"]["wspolrzedne"])
                osobnik["przenoszone"] = None
                osobnik["cel"] = None
            else:
                przesun_osobnika(osobnik, osobnik["cel"])  # Zmieniłem nazwę funkcji tutaj



def oblicz_punktacje(kolonie):
    punktacja = 0
    for kolonia in kolonie:
        for zasob in kolonia["magazyn"]:
            punktacja += zasob["wartosc"]
    return punktacja



def przenies_zasob(zasob):
    for typ in zasoby:
        if zasob in zasoby[typ]:
            zasoby[typ].remove(zasob)
            break

# Generowanie mapy przed rozpoczęciem gry
generuj_zasoby()

# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    rysuj()

    aktualizuj_pozycje_kolonii(punktacja, kolonia_a, kolonia_b, zasoby, magazyny)


    pygame.time.delay(50)

pygame.quit()