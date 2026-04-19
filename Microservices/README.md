# Microservices - przykład architektury mikroserwisowej

Ten katalog pokazuje minimalny przykład architektury **microservices** dla scenariusza tworzenia zamówienia.

W aktualnym kodzie są trzy punkty wejścia:

- `users-service` - zwraca dane użytkownika,
- `orders-service` - przyjmuje zamówienie, dopytuje `users-service` o użytkownika i buduje odpowiedź,
- `main.py` w katalogu głównym - prosty klient/orchestrator wywołujący `orders-service`.

## Co jest w kodzie

```text
Microservices/
├── main.py
├── requirements.txt
├── orders-service/
│   └── main.py
├── users-service/
│   └── main.py
└── tests/
    └── test_services.py
```

## Rola plików

- `users-service/main.py`  
  FastAPI z endpointem `GET /users/{user_id}`. Zwraca `UserForOrderDto` zawierające `user_id` i `user_name`.

- `orders-service/main.py`  
  FastAPI z endpointem `POST /orders`. Serwis:
  1. przyjmuje `user_id` i `product`,
  2. wywołuje `GET http://127.0.0.1:8002/users/{user_id}` przez `requests`,
  3. waliduje odpowiedź przy pomocy `UserForOrderDto` z Pydantic,
  4. zwraca finalne dane zamówienia z `user_name`.

- `main.py`  
  Nie jest serwisem HTTP. To zwykły skrypt-klient z funkcją `run(...)`, która wysyła `POST` do `orders-service` i wypisuje odpowiedź jako JSON.

- `requirements.txt`  
  Zawiera zależności potrzebne do uruchomienia serwisów i testów: `fastapi`, `uvicorn`, `pytest`, `httpx`, `requests`.

- `tests/test_services.py`  
  Testuje:
  - endpoint `users-service`,
  - endpoint `orders-service` z podmienionym wywołaniem HTTP,
  - skrypt `main.py`,
  - propagację błędu HTTP z `orders-service`.

## Endpointy

### Users Service

`GET /users/{user_id}`

Przykładowa odpowiedź:

```json
{
  "user_id": 1,
  "user_name": "Marcin"
}
```

### Orders Service

`POST /orders`

Przykładowe body:

```json
{
  "user_id": 1,
  "product": "Laptop"
}
```

Przykładowa odpowiedź:

```json
{
  "user_id": 1,
  "user_name": "Marcin",
  "product": "Laptop"
}
```

## Przepływ działania

1. Klient wywołuje `POST /orders` w `orders-service`.
2. `orders-service` wywołuje `users-service` po `user_id`.
3. `users-service` zwraca `user_name`.
4. `orders-service` składa odpowiedź zamówienia i odsyła ją klientowi.
5. Główny `main.py` może zostać użyty do pokazania tego przepływu z poziomu zwykłego skryptu.

## Jak uruchamiać

Najpierw zainstaluj zależności z katalogu `Microservices/`:

```powershell
py -3 -m pip install -r requirements.txt
```

Uruchom `users-service` w katalogu `Microservices/users-service/`:

```powershell
uvicorn main:app --reload --port 8002
```

Uruchom `orders-service` w katalogu `Microservices/orders-service/`:

```powershell
uvicorn main:app --reload --port 8001
```

Następnie z katalogu `Microservices/` uruchom klienta:

```powershell
py -3 main.py
```

## Jak uruchomić testy

Z katalogu `Microservices/`:

```powershell
py -3 -m pytest tests -q
```

## Co ten przykład pokazuje

- osobne procesy HTTP dla różnych odpowiedzialności,
- komunikację synchroniczną między serwisami przez HTTP,
- walidację odpowiedzi między serwisami przy pomocy Pydantic,
- prosty klient wywołujący cały przepływ.

## Czego ten przykład jeszcze nie pokazuje

- service discovery,
- retry/circuit breaker,
- osobnych baz danych per service,
- autoryzacji i observability,
- asynchronicznej komunikacji między serwisami.
