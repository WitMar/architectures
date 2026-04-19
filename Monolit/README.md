# Monolit - przykład modularnego monolitu

Ten katalog pokazuje prosty przykład **modular monolith**.

Cały system działa jako jeden proces, ale kod jest podzielony na osobne moduły biznesowe:

- `users` - odpowiedzialny za użytkownika,
- `orders` - odpowiedzialny za zamówienia,
- `contracts` - wspólny kontrakt danych przekazywanych między modułami,
- `app/main.py` - miejsce, w którym moduły są spinane.

## Co jest w kodzie

```text
Monolit/
├── app/
│   ├── main.py
│   ├── contracts/
│   │   └── user_for_order_dto.py
│   ├── orders/
│   │   ├── model.py
│   │   └── service.py
│   └── users/
│       ├── model.py
│       └── service.py
└── README.md
```

## Rola plików

- `app/users/model.py`  
  Model `User` z polami `user_id`, `name`, `email`, `roles`.

- `app/users/service.py`  
  `UserService.get_user_for_order(...)` buduje obiekt `User`, a następnie mapuje go do `UserForOrderDto`.

- `app/contracts/user_for_order_dto.py`  
  DTO używane jako kontrakt między modułem `users` i `orders`. Zawiera `user_id`, `user_name`, `user_email`.

- `app/orders/model.py`  
  Model `Order` z polami `user_id`, `user_name`, `product`.

- `app/orders/service.py`  
  `OrderService.create_order(...)` przyjmuje `UserForOrderDto` zamiast modelu `User`, dzięki czemu moduł `orders` nie zależy bezpośrednio od wewnętrznego modelu modułu `users`.

- `app/main.py`  
  Warstwa integracyjna. Pobiera DTO z `users`, przekazuje je do `orders` i wypisuje utworzone zamówienie.

## Przepływ działania

1. `UserService.get_user_for_order(1)` tworzy użytkownika `Marcin`.
2. Dane są mapowane do `UserForOrderDto`.
3. `OrderService.create_order(user_dto, "Laptop")` tworzy zamówienie.
4. `app/main.py` wypisuje wynik w formacie:
   `Order: user=Marcin (id=1), product=Laptop`.

## Co ten przykład pokazuje

- jeden proces, ale wyraźne granice modułów,
- komunikację między modułami przez DTO/kontrakt,
- brak bezpośredniego przekazywania modelu `User` do modułu `orders`,
- jedno miejsce integracji w `app/main.py`.

## Jak uruchamiać

`app/main.py` importuje moduły jako `users.service` i `orders.service`, więc uruchamiaj z katalogu `Monolit/app/`:

```powershell
py -3 main.py
```

## Testy

W aktualnym katalogu `Monolit/` nie ma osobnego folderu `tests`.

## Czego ten przykład jeszcze nie pokazuje

- bazy danych,
- API HTTP,
- zdarzeń domenowych,
- niezależnego wdrażania modułów,
- testów automatycznych dla granic modułów.
