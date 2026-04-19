LayerdArchitecture - przykład architektury warstwowej
====================================================

Przykład pokazuje podstawową wersję **architektury warstwowej** dla scenariusza:

- pobranie danych użytkownika,
- utworzenie zamówienia,
- praca na prostym modelu domenowym `Order`.

W tej wersji skupiamy się przede wszystkim na układzie warstw, a nie na pełnej funkcjonalności aplikacji.

Struktura katalogów
-------------------


    LayerdArchitecture/
      app/
        application/
          create_order.py
        domain/
          order.py
        infrastructure/
          order_repository.py
        presentation/
          api.py
      tests/
        test_layered_architecture.py

Rola poszczególnych warstw
--------------------------

`domain`
    Zawiera model domenowy `Order`. To tutaj znajduje się podstawowy obiekt biznesowy.

`application`
    Zawiera przypadek użycia `create_order`, który buduje obiekt domenowy na podstawie przekazanych danych.

`presentation`
    Zawiera prosty punkt wejścia `api.py`, który uruchamia przykład i wypisuje wynik.

`infrastructure`
    W tej wersji zawiera jedynie prosty placeholder `OrderRepository`, przygotowany pod kolejną iterację z zapisem danych.

Co pokazuje ten przykład?
-------------------------

To jest **wersja podstawowa** architektury warstwowej z materiałów:

- warstwa prezentacji wywołuje przypadek użycia,
- warstwa aplikacyjna korzysta z modelu domenowego,
- logika jest podzielona według odpowiedzialności,
- całość nadal działa jako jedna aplikacja.

Jak uruchomić?
--------------

Uruchom przykład z katalogu `LayerdArchitecture/`:

    py -3 -m app.presentation.api

Oczekiwany wynik:

    Marcin Laptop

Jak uruchomić test?
-------------------

    py -3 -m unittest discover -s tests -p "test_*.py"

Czego ten przykład jeszcze nie pokazuje?
----------------------------------------

To jest wersja startowa, dlatego nie zawiera jeszcze:

- walidacji biznesowej w modelu domenowym,
- zapisu do bazy danych,
- integracji z API,
- bardziej złożonych przypadków użycia,
- DTO lub osobnych modeli wejścia/wyjścia.

Te elementy są rozwijane w dalszej części materiałów.


