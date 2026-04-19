EventBased - przykład architektury zdarzeniowej
==============================================

Ten katalog zawiera **podstawową implementację** architektury event-driven:

- prosty `EventBus`,
- moduł `orders`, który publikuje zdarzenie `OrderCreated`,
- moduł `notifications`, który reaguje na zdarzenie,
- punkt uruchomieniowy spinający cały przepływ.

Scenariusz przykładowy
----------------------

W przykładzie realizujemy następujący scenariusz:

- tworzymy zamówienie dla użytkownika `Marcin`,
- moduł `orders` publikuje zdarzenie `OrderCreated`,
- moduł `notifications` odbiera zdarzenie i wysyła potwierdzenie.

Struktura katalogów
-------------------

    EventBased/
      app/
        main.py
        events/
          bus.py
        orders/
          service.py
        notifications/
          handler.py
      tests/
        test_event_based_smoke.py

Opis elementów
--------------

`app/events/bus.py`
    Zawiera klasę `EventBus` z metodami `subscribe()` i `publish()`.

`app/orders/service.py`
    Zawiera `OrderService`, który tworzy zamówienie i publikuje zdarzenie `OrderCreated`.

`app/notifications/handler.py`
    Zawiera handler `send_order_confirmation(order)`, reagujący na zdarzenie.

`app/main.py`
    Składa obiekty, rejestruje handler i uruchamia przykładowy przepływ.

`tests/test_event_based_smoke.py`
    Prosty test smoke sprawdzający, że publikacja zdarzenia wywołuje handler.

Co pokazuje ten przykład?
-------------------------

Najważniejsza idea architektury zdarzeniowej jest taka, że:

- producent zdarzenia nie zna bezpośrednio konsumenta,
- nowe reakcje można dodawać bez zmiany modułu `orders`,
- komunikacja odbywa się przez zdarzenie, a nie bezpośrednie wywołanie metody.

Jak uruchomić?
--------------

Uruchom przykład z katalogu `EventBased/`:

    py -3 -m app.main

Przykładowy wynik:

    Sending notification for Marcin and product Laptop
    {'user_id': 1, 'user_name': 'Marcin', 'product': 'Laptop'}

Jak uruchomić test?
-------------------

    py -3 -m unittest discover -s tests -p "test_*.py"

Czego ten przykład jeszcze nie pokazuje?
----------------------------------------

To jest wersja podstawowa, więc nie zawiera jeszcze:

- wielu różnych subskrybentów jednego zdarzenia,
- osobnych klas zdarzeń lub DTO dla payloadu,
- kolejki lub brokera wiadomości,
- idempotencji i obsługi błędów konsumentów,
- asynchronicznego przetwarzania.

Te elementy można dopisać w kolejnych iteracjach.

