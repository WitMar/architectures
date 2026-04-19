# LayeredArchitecture - przykład architektury warstwowej

Ten katalog pokazuje prosty przykład **layered architecture** dla tworzenia zamówienia.

Kod jest rozdzielony na cztery warstwy:

- `presentation` - punkt wejścia aplikacji,
- `application` - przypadek użycia `create_order(...)`,
- `domain` - model biznesowy `Order`,
- `infrastructure` - repozytorium zapisujące zamówienie.

## Co jest w kodzie

```text
LayeredArchitecture/
├── app/
│   ├── application/
│   │   └── create_order.py
│   ├── domain/
│   │   └── order.py
│   ├── infrastructure/
│   │   └── order_repository.py
│   └── presentation/
│       └── api.py
└── tests/
    └── test_layered_architecture.py
```

## Rola warstw i plików

- `app/presentation/api.py`  
  Najprostszy entrypoint. Wywołuje `create_order(...)` i wypisuje `user_name` oraz `product`.

- `app/application/create_order.py`  
  Zawiera funkcję `create_order(...)`, która tworzy obiekt domenowy `Order`, tworzy repozytorium `OrderRepository`, zapisuje zamówienie i zwraca wynik.

- `app/domain/order.py`  
  Model domenowy `Order`. Aktualnie zawiera też prostą walidację: gdy `product` jest pusty, rzuca `ValueError("Product name is required")`.

- `app/infrastructure/order_repository.py`  
  Minimalna warstwa infrastruktury. `save(...)` tylko wypisuje informację o zapisie zamówienia.

- `tests/test_layered_architecture.py`  
  Sprawdza, że `create_order(...)` zwraca poprawnie zbudowany obiekt `Order`.

## Przepływ działania

1. `presentation/api.py` wywołuje `create_order(1, "Marcin", "Laptop")`.
2. Warstwa aplikacyjna tworzy domenowy `Order`.
3. Model domenowy wykonuje walidację danych.
4. Warstwa infrastruktury zapisuje zamówienie.
5. Wynik wraca do warstwy prezentacji i jest wypisywany.

## Co ten przykład pokazuje

- podział odpowiedzialności na warstwy,
- oddzielenie modelu domenowego od prezentacji,
- prostą orkiestrację w warstwie aplikacyjnej,
- miejsce, w którym można później podmienić infrastrukturę na bazę danych lub API.

## Jak uruchamiać

`app/presentation/api.py` importuje moduły przez prefiks `LayeredArchitecture`, więc najprościej uruchamiać z katalogu nadrzędnego workspace:

```powershell
py -3 -m LayeredArchitecture.app.presentation.api
```

## Jak uruchomić testy

Z katalogu nadrzędnego workspace:

```powershell
py -3 -m pytest LayeredArchitecture/tests -q
```

## Czego ten przykład jeszcze nie pokazuje

- trwałego zapisu do bazy danych,
- osobnych DTO lub commandów wejściowych,
- dependency injection,
- bardziej rozbudowanych przypadków użycia,
- testów izolujących infrastrukturę od aplikacji.
