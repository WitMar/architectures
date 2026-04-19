Heksagonal - przykład architektury heksagonalnej
================================================

Ten katalog zawiera **początkową implementację** przykładu architektury heksagonalnej.

- rdzeń domeny (`domain`),
- przypadek użycia (`application`),
- porty (`ports`),
- adaptery in-memory (`adapters`).

Scenariusz przykładowy
----------------------

W przykładzie realizujemy ten sam scenariusz co w materiałach:

- pobieramy użytkownika o identyfikatorze `1`,
- tworzymy zamówienie na produkt `Laptop`,
- zapisujemy zamówienie przez adapter repozytorium.

Struktura katalogów
-------------------

    Heksagonal/
      app/
        application/
          create_order.py
        domain/
          order.py
        ports/
          user_query_port.py
          order_repository_port.py
        adapters/
          users_in_memory.py
          orders_in_memory.py
          api.py
      tests/
        test_hexagonal_architecture.py

Opis elementów
--------------

`app/domain/order.py`
    Model domenowy `Order`.

`app/ports/user_query_port.py`
    Port wejścia do pobierania danych użytkownika potrzebnych do utworzenia zamówienia.

`app/ports/order_repository_port.py`
    Port odpowiedzialny za zapis zamówienia.

`app/application/create_order.py`
    Przypadek użycia `CreateOrderUseCase`, który korzysta wyłącznie z portów i nie zna szczegółów technologicznych.

`app/adapters/users_in_memory.py`
    Adapter in-memory zwracający dane użytkownika.

`app/adapters/orders_in_memory.py`
    Adapter in-memory zapisujący zamówienie do listy w pamięci.

`app/adapters/api.py`
    Prosty punkt uruchomieniowy składający adaptery i uruchamiający przypadek użycia.

Co pokazuje ten przykład?
-------------------------

Najważniejsza idea architektury heksagonalnej jest taka, że:

- logika biznesowa nie zależy od bazy danych,
- logika biznesowa nie zależy od frameworka webowego,
- technologia jest podłączana przez adaptery,
- rdzeń systemu można testować w izolacji.

Jak uruchomić?
--------------

Uruchom przykład z katalogu `Heksagonal/`:

    py -3 -m app.adapters.api

Przykładowy wynik:

    Saving order: 1 Laptop
    Marcin Laptop

Jak uruchomić test?
-------------------

    py -3 -m unittest discover -s tests -p "test_*.py"

Czego ten przykład jeszcze nie pokazuje?
----------------------------------------

To jest wersja początkowa, więc nie zawiera jeszcze:

- adaptera HTTP,
- adaptera bazy danych,
- walidacji błędów integracyjnych,
- bardziej rozbudowanego modelu domenowego,
- osobnego API webowego.

Te elementy można dopisać w kolejnych iteracjach bez zmiany rdzenia biznesowego.

