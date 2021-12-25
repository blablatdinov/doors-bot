# Как пользоваться?

```
python3.9 -m venv venv
pip install -r requirements.txt
```

Можно удалить директорию blog, и стереть из INSTALLED_APPS

Запуск тестов:

```
make test
# или
pytest
```

Запуск сортировки импортов и линтера

```
make lint
# или
isort . && flake8 .
```