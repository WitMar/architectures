# EventBased - przykład architektury zdarzeniowej

Ten katalog pokazuje prosty przykład **event-driven workflow** z kompensacją:

- moduł `orders` zapisuje zamówienie i publikuje `OrderCreated`,
- moduł `loyalty` niezależnie próbuje zapisać punkty,
- po sukcesie loyalty publikuje `LoyaltyPointsAdded`,
- moduł `orders` zmienia status na `PROCESSED` i publikuje `OrderProcessed`,
- moduł `notifications` wysyła potwierdzenie dopiero po `OrderProcessed`,
- gdy zapis punktów się nie uda, `orders` oznacza zamówienie jako `RETRACTED` i potwierdzenie nie jest wysyłane.

## Co jest w kodzie

```text
EventBased/
├── app/
│   ├── main.py
│   ├── events/
│   │   ├── bus.py
│   │   ├── dto.py
│   │   └── outbox_publisher.py
│   ├── loyalty/
│   │   └── handler.py
│   ├── notifications/
│   │   └── handler.py
│   └── orders/
│       ├── handler.py
│       └── service.py
└── tests/
    └── test_event_based_smoke.py
```

## Rola plików

- `app/main.py`  
  Składa cały przykład w pamięci: tworzy `EventBus`, dwa outboxy (`orders` i `loyalty`), repozytorium zamówień oraz rejestruje subskrypcje. Zawiera też helper `publish_all_pending_events(...)`, który opróżnia outboxy aż workflow się zakończy.

- `app/events/bus.py`  
  Minimalny, synchroniczny event bus z `subscribe()` i `publish()`.

- `app/events/outbox_publisher.py`  
  Czyta wiadomości o statusie `NEW`, publikuje je na busie i oznacza jako `PUBLISHED`.

- `app/events/dto.py`  
  Zawiera klasy DTO pozostawione w katalogu, ale bieżący przepływ korzysta już głównie z prostych słowników jako payloadów zdarzeń.

- `app/orders/service.py`  
  Tworzy zamówienie ze statusem `PENDING_LOYALTY`, zapisuje je i odkłada zdarzenie `OrderCreated` do outboxa `orders`.

- `app/orders/handler.py`  
  Reaguje na wynik procesu loyalty:
  - `mark_order_as_processed(...)` ustawia status `PROCESSED` i publikuje `OrderProcessed`,
  - `retract_order(...)` ustawia status `RETRACTED`.

- `app/loyalty/handler.py`  
  Zapisuje punkty lojalnościowe i publikuje wynik do outboxa `loyalty`:
  - `LoyaltyPointsAdded` przy sukcesie,
  - `LoyaltyPointsSaveFailed` przy błędzie.  
  Plik zawiera też prostą idempotencję (`points_were_already_added(...)`) oraz flagę testową `should_fail_to_save_points`.

- `app/notifications/handler.py`  
  Wysyła potwierdzenie tylko dla zdarzenia `OrderProcessed`.

- `tests/test_event_based_smoke.py`  
  Sprawdza trzy scenariusze:
  - pełny happy path,
  - idempotentny zapis punktów,
  - rollback biznesowy: `RETRACTED` bez potwierdzenia.

## Przepływ działania

1. `OrderService.create_order(...)` zapisuje zamówienie i odkłada `OrderCreated` do outboxa `orders`.
2. `OutboxPublisher` publikuje `OrderCreated`.
3. `loyalty.handler.register_loyalty_points(...)` próbuje zapisać punkty.
4. Loyalty publikuje jedno z dwóch zdarzeń:
   - `LoyaltyPointsAdded`, albo
   - `LoyaltyPointsSaveFailed`.
5. `orders.handler` reaguje na wynik:
   - sukces -> status `PROCESSED` + `OrderProcessed`,
   - porażka -> status `RETRACTED`.
6. `notifications.handler.send_order_confirmation(...)` działa tylko po `OrderProcessed`.

## Co ten przykład pokazuje

- niezależne kroki procesu połączone zdarzeniami,
- lokalny outbox jako prosty mechanizm niezawodnego publikowania,
- kompensację zamiast jednej wspólnej transakcji między procesami,
- jawne statusy procesu: `PENDING_LOYALTY`, `PROCESSED`, `RETRACTED`.

## Jak uruchamiać

Aktualne importy w `app/main.py` używają prefiksu `EventBased`, więc najprościej uruchamiać przykład z katalogu nadrzędnego workspace:

```powershell
py -3 -m EventBased.app.main
```

## Jak uruchomić testy

Z katalogu nadrzędnego workspace:

```powershell
py -3 -m pytest EventBased/tests -q
```

## Czego ten przykład jeszcze nie pokazuje

- prawdziwego brokera wiadomości,
- trwałego outboxa w bazie danych,
- osobnych procesów/workerów dla `orders`, `loyalty` i `notifications`,
- retry/backoff i dead-letter queue,
- monitoringu i observability.
