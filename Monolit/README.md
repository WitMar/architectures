Modularny monolit - przykład
============================

Ten katalog zawiera **bardzo prosty przykład modularnego monolitu**.

Celem przykładu nie jest pokazanie pełnej aplikacji produkcyjnej, tylko zademonstrowanie podstawowej idei:

- system działa jako **jedna aplikacja**,
- kod jest podzielony na **moduły biznesowe**,
- moduły mają własne modele i serwisy,
- integracja między nimi odbywa się w jednym miejscu.

Struktura katalogów
-------------------

::

    Monolit/
      app/
        main.py
        users/
          model.py
          service.py
        orders/
          model.py
          service.py

Opis elementów
--------------

`app/users/model.py`
    Definiuje obiekt `User`.

`app/users/service.py`
    Zawiera `UserService`, który zwraca przykładowego użytkownika.

`app/orders/model.py`
    Definiuje obiekt `Order`.

`app/orders/service.py`
    Zawiera `OrderService`, który tworzy zamówienie.

`app/main.py`
    Pełni rolę **warstwy integracyjnej**. To tutaj pobierany jest użytkownik z modułu `users`, a następnie jego identyfikator przekazywany do modułu `orders` w celu utworzenia zamówienia.

Przepływ działania
------------------

1. `UserService.get_user(1)` zwraca użytkownika `Marcin`.
2. `OrderService.create_order(...)` tworzy zamówienie na produkt `Laptop`.
3. `main.py` wypisuje dane użytkownika i zamówienia.

Dzięki temu widać podstawową zasadę modularnego monolitu: moduły są rozdzielone logicznie, ale cały system nadal uruchamia się jako jeden proces.

Uruchomienie
------------

Uruchamiaj przykład z katalogu `app/`, ponieważ importy w `main.py` zakładają właśnie taki punkt startu.



    cd app
    py -3 main.py

Przykładowy wynik:


    1 Marcin
    1 Laptop

Czego ten przykład jeszcze nie pokazuje?
---------------------------------------

To jest wersja podstawowa. Przykład **nie pokazuje jeszcze**:

- przekazywania bardziej złożonych danych użytkownika do zamówienia,
- DTO między modułami,
- walidacji biznesowej,
- zapisu do bazy danych,
- testów automatycznych.

Te rozszerzenia są opisane w materiałach.

Czego unikać?
-------------

W modularnym monolicie warto unikać:

- bezpośredniego importowania modeli jednego modułu do wnętrza drugiego modułu,
- mieszania odpowiedzialności między `users` i `orders`,
- traktowania samego podziału katalogów jako pełnej architektury.

Najważniejsza idea jest prosta: **jeden system, ale wyraźne granice modułów**.

