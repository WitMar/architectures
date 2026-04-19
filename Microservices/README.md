# Microservices example

Minimalny przykład pokazujący podstawową strukturę mikroserwisów.

## Struktura

```text
Microservices/
├── users-service/
│   └── main.py
├── orders-service/
│   └── main.py
├── tests/
│   └── test_services.py
└── requirements.txt
└── main.py
```

## Co pokazuje ten przykład

To jest **wersja podstawowa** architektury mikroserwisowej:

- `users-service` udostępnia dane użytkownika,
- `orders-service` przyjmuje komplet danych potrzebnych do utworzenia zamówienia,
- oba serwisy są rozdzielone na osobne procesy i mogą być uruchamiane niezależnie.

Jest to odpowiednik przykładu z (`Modularny monolit`), ale rozbity na dwa osobne serwisy.

## Endpointy

### Users Service

- `GET /users/{user_id}`

Przykładowa odpowiedź:

```json
{
  "user_id": 1,
  "user_name": "Marcin"
}
```

### Orders Service

- `POST /orders`

Przykładowe body:

```json
{
  "user_id": 1,
  "user_name": "Marcin",
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

## Instalacja

```bash
pip install -r requirements.txt
```

## Uruchomienie lokalne

W PyCharm w run configuration wybierz tym module: uvicorn i w polu parametrów skryptu wpisz  main:app --reload --port 8001.

Uruchom `users-service`:

```bash
uvicorn main:app --reload --port 8001
```

w katalogu `users-service/`.

W PyCharm w run configuration wybierz tym module: uvicorn i w polu parametrów skryptu wpisz  main:app --reload --port 8002.

Uruchom `orders-service`:

```bash
uvicorn main:app --reload --port 8002
```

w katalogu `orders-service/`.

Uruchom main.py z głównego katalogu, aby zobaczyć przykładowy przepływ działania obu serwisów.

## Testy smoke

```bash
pytest
```

Testy sprawdzają podstawowe działanie obu endpointów bez potrzeby ręcznego uruchamiania serwisów.

