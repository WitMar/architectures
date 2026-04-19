 EventBased - przykład architektury zdarzeniowej
==============================================

Ten katalog zawiera **podstawową implementację** architektury event-driven z prostą kompensacją:

- prosty `EventBus`,
- moduł `orders`, który zapisuje zamówienie i publikuje zdarzenie `OrderCreated`,
- moduł `loyalty`, który niezależnie próbuje zapisać punkty i publikuje sukces albo porażkę,
- moduł `notifications`, który reaguje dopiero na potwierdzone zamówienie,
- punkt uruchomieniowy spinający cały przepływ.

Scenariusz przykładowy
----------------------

W przykładzie realizujemy następujący scenariusz:

- tworzymy zamówienie dla użytkownika `Marcin`,
- moduł `orders` publikuje zdarzenie `OrderCreated`,
- moduł `loyalty` niezależnie zapisuje punkty i publikuje `LoyaltyPointsAdded`,
- moduł `orders` aktualizuje status zamówienia na `PROCESSED`,
- moduł `notifications` wysyła potwierdzenie po zakończeniu przepływu,
- jeżeli zapis punktów się nie uda, zamówienie zostaje oznaczone jako `RETRACTED` i nie ma potwierdzenia.

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

`app/orders/handler.py`
    Zawiera handlery `mark_order_as_processed(...)` i `retract_order(...)`, reagujące na wynik procesu loyalty.

`app/loyalty/handler.py`
    Zawiera handler `register_loyalty_points(...)`, który zapisuje punkty i zapisuje do własnego outboxa zdarzenie sukcesu albo porażki.

`app/notifications/handler.py`
    Zawiera handler `send_order_confirmation(order)`, reagujący na zdarzenie `OrderProcessed`.

`app/main.py`
    Składa obiekty, rejestruje handler i uruchamia przykładowy przepływ.

`tests/test_event_based_smoke.py`
    Prosty test smoke sprawdzający, że publikacja zdarzenia wywołuje handler.

Co pokazuje ten przykład?
-------------------------

Najważniejsza idea architektury zdarzeniowej jest taka, że:

- producent zdarzenia nie zna bezpośrednio konsumenta,
- nowe reakcje można dodawać bez zmiany modułu `orders`,
- komunikacja odbywa się przez zdarzenie, a nie bezpośrednie wywołanie metody,
- kolejne etapy procesu mogą publikować następne zdarzenia (`OrderCreated` -> `LoyaltyPointsAdded` -> `OrderProcessed`),
- porażka w jednym niezależnym kroku może uruchomić prostą kompensację (`RETRACTED`).

Jak uruchomić?
--------------

Uruchom przykład z katalogu `EventBased/`:

    py -3 -m app.main

Przykładowy wynik:

    Saving order to DB {'order_id': 101, 'user_id': 1, 'user_name': 'Marcin', 'product': 'Laptop', 'status': 'PENDING_LOYALTY'}
    Saving points for user 1 order id 101
    Sending notification for done order for Marcin and product Laptop
    Order :  {'order_id': 101, 'user_id': 1, 'user_name': 'Marcin', 'product': 'Laptop', 'status': 'PROCESSED'}

Jak uruchomić test?
-------------------

    py -3 -m unittest discover -s tests -p "test_*.py"

Czego ten przykład jeszcze nie pokazuje?
----------------------------------------

To jest wersja podstawowa, więc nie zawiera jeszcze:

- wielu różnych subskrybentów jednego zdarzenia,
- osobnych klas zdarzeń lub DTO dla payloadu,
- kolejki lub brokera wiadomości,
- pełnej trwałości pomiędzy restartami procesu,
- asynchronicznego przetwarzania.

Te elementy można dopisać w kolejnych iteracjach.

