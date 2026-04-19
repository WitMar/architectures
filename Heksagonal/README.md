# Heksagonal - przykład architektury heksagonalnej

Ten katalog pokazuje prosty przykład **hexagonal architecture / ports & adapters** dla tworzenia zamówienia.

Aktualny kod jest podzielony na:

- `domain` - model biznesowy `Order`,
- `application` - przypadek użycia `CreateOrderUseCase` i DTO wejściowe z modułu użytkowników,
- `ports` - kontrakty wymagane przez use case,
- `adapters` - kilka wymiennych adapterów do pobierania użytkownika i zapisu zamówienia.

## Co jest w kodzie

```text
Heksagonal/
├── app/
│   ├── adapters/
│   │   ├── api.py
│   │   ├── order_sql.py
│   │   ├── orders_file.py
│   │   ├── orders_in_memory.py
│   │   ├── users_http.py
│   │   └── users_in_memory.py
│   ├── application/
│   │   ├── create_order.py
│   │   └── user_for_order_dto.py
│   ├── domain/
│   │   └── order.py
│   └── ports/
│       ├── order_repository_port.py
│       └── user_query_port.py
└── tests/
    └── test_hexagonal_architecture.py
```

## Rola plików

- `app/domain/order.py`  
  Najprostszy model domenowy `Order` z polami `user_id`, `user_name`, `product`.

- `app/application/create_order.py`  
  Definiuje `CreateOrderUseCase`. Use case:
  1. pobiera użytkownika przez `user_query_port`,
  2. tworzy domenowy `Order`,
  3. zapisuje go przez `order_repository_port`.

- `app/application/user_for_order_dto.py`  
  DTO `UserForOrderDto`, czyli minimalny zestaw danych potrzebnych do złożenia zamówienia.

- `app/ports/user_query_port.py`  
  Port do pobierania danych użytkownika potrzebnych do zamówienia.

- `app/ports/order_repository_port.py`  
  Port do zapisu zamówienia.

- `app/adapters/users_in_memory.py`  
  Adapter testowy/in-memory zwracający użytkownika `Marcin`.

- `app/adapters/users_http.py`  
  Adapter udający wywołanie zewnętrznego serwisu użytkowników (`print("GET http://users-service/users/{user_id}")`).

- `app/adapters/orders_in_memory.py`  
  Adapter zapisujący zamówienia do listy `saved_orders` w pamięci.

- `app/adapters/orders_file.py`  
  Adapter zapisujący zamówienia do pliku `orders.txt`.

- `app/adapters/order_sql.py`  
  Adapter wypisujący przykładowe polecenie SQL `INSERT INTO orders ...`.

- `app/adapters/api.py`  
  Prosty entrypoint składający use case z adapterem HTTP po stronie użytkownika oraz adapterem SQL po stronie zamówień.

- `tests/test_hexagonal_architecture.py`  
  Testuje rdzeń aplikacyjny z adapterami in-memory, bez zależności od HTTP i SQL.

## Przepływ działania

1. `CreateOrderUseCase.execute(...)` woła `user_query_port.get_user_for_order(...)`.
2. Adapter użytkownika zwraca `UserForOrderDto`.
3. Use case tworzy `Order`.
4. `order_repository_port.save(order)` zapisuje zamówienie przez wybrany adapter.

## Co ten przykład pokazuje

- use case zależy od portów, a nie od technologii,
- adaptery można swobodnie podmieniać,
- testy mogą uruchamiać logikę biznesową wyłącznie na adapterach in-memory,
- HTTP / SQL / plik są tylko szczegółami implementacyjnymi na brzegu systemu.

## Jak uruchamiać

`app/adapters/api.py` importuje moduły przez prefiks `Heksagonal`, więc najprościej uruchamiać z katalogu nadrzędnego workspace:

```powershell
py -3 -m Heksagonal.app.adapters.api
```

## Jak uruchomić testy

Z katalogu nadrzędnego workspace:

```powershell
py -3 -m pytest Heksagonal/tests -q
```

## Czego ten przykład jeszcze nie pokazuje

- prawdziwego klienta HTTP,
- prawdziwej bazy danych,
- walidacji błędów integracyjnych,
- dependency injection przez framework,
- bogatszego modelu domenowego.
