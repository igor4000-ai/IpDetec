# 🌍 IpDetec

![Python](https://img.shields.io/badge/Python-3.14%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Language](https://img.shields.io/badge/Language-Russian-blue)
![GitHub stars](https://img.shields.io/github/stars/igor4000-ai/IpDetec)
![GitHub forks](https://img.shields.io/github/forks/igor4000-ai/IpDetec)

Утилита для определения IP-адреса, геолокации и автоматической загрузки информации на Яндекс.Диск.

## ✨ Возможности

- 🔍 Определение IP-адреса — автоматическое определение Вашего текущего IP-адреса
- 🏙️ Геолокация — получение информации о городе по IP-адресу
- 💾 Сохранение данных — автоматическое сохранение полученной информации в JSON-формат
- ☁️ Интеграция с Яндекс.Диском — автоматическая загрузка файлов в облачное хранилище
- 🗂️ Умная организация — создание отдельных папок для каждого города
- 🧹 Автоматическая очистка — удаление локальных файлов после успешной загрузки

## 📋 Требования

- Python 3.14 или выше
- Учетная запись Яндекс.Диск
- API-ключ для Яндекс.Диска

## 🚀 Установка

### Клонирование репозитория

```bash
git clone https://github.com/igor4000-ai/IpDetec.git
cd IpDetec
```

### Установка зависимостей

#### С использованием uv (рекомендуется)

```bash
# Установка uv (если еще не установлен)
pip install uv

# Синхронизация окружения с pyproject.toml
uv sync
```

#### С использованием pip

```bash
# Создание виртуального окружения
python -m venv venv

# Активация виртуального окружения
# На Linux/Mac:
source venv/bin/activate
# На Windows:
venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt
```

### Настройка API-ключа Яндекс.Диска

1. Получите API-ключ на странице Яндекс.Диска: https://yandex.ru/dev/disk/poligon/
2. При запуске программы ключ будет запрошен в консоли


## 📖 Использование

### Базовый запуск

```bash
python main.py
```

### Пример вывода

```
Введите ключ от Яндекс.Диска: <ваш_токен>
IP-адрес успешно получен: 111.111.111.111
Информация о городе успешно получена: Helsinki
Данные сохранены в файл: info.json
Папка Helsinki готова для загрузки
Ссылка для загрузки успешно получена для пути: Helsinki/info.json
Файл успешно загружен на Яндекс.Диск. Статус: 201
Локальный файл info.json успешно удален
Ваш IP-адрес: 111.111.111.111
Ваш город: Helsinki
```

## 🏗️ Архитектура проекта

```
IpDetec/
├── main.py              # Точка входа, содержит только функцию main()
├── core.py              # Основная логика и классы приложения
├── config.py            # Конфигурация приложения
├── api_key.py           # Запрос API-ключа 
├── pyproject.toml       # Зависимости проекта (для uv)
├── requirements.txt     # Зависимости Python (для pip)
└── README.md            # Документация
```

## 📚 Основные компоненты (модуль core.py)

### IPInfoAPI
Класс для получения текущего IP-адреса.

- `get_ip()` — получает текущий IP-адрес

### CityInfoAPI
Класс для получения информации о городе по IP-адресу.

- `get_city()` — получает информацию о городе и кеширует IP
- `get_saved_ip()` — возвращает сохраненный IP-адрес 

### FileManager
Менеджер для работы с локальными файлами.

- `save_json(data)` — сохраняет данные в JSON-файл
- `remove_file()` — удаляет локальный файл
- `file_name()` — возвращает имя файла

### YandexDiskUploader
Класс для загрузки файлов на Яндекс.Диск.

- `get_upload_link(city)` — получает ссылку для загрузки файла (создает папку города при необходимости)
- `upload_file(city)` — загружает файл на Яндекс.Диск в папку с именем города

## 🔧 Конфигурация

Основные настройки находятся в файле `config.py` и соответствуют коду:

```python
from typing import Dict, Any


class Config:
    """Конфигурационные настройки приложения."""

    # API endpoints
    URL_IP: str = 'https://api.ipify.org'
    BASE_URL_CITY: str = 'https://ipinfo.io'
    URL_YD: str = 'https://cloud-api.yandex.net'
    LINK_DL_FILE: str = 'https://cloud-api.yandex.net/v1/disk/resources/upload'

    # Файловые настройки
    FILE_NAME: str = 'info.json'

    # Настройки запросов
    REQUEST_TIMEOUT: int = 5  # секунды

    # Параметры для загрузки на Яндекс.Диск
    UPLOAD_PARAMS: Dict[str, Any] = {
        'path': FILE_NAME,
        'fields': 'href',
        'overwrite': True
    }
```

## 🧪 Проверка

- Старт приложения: `python main.py` (ввод токена будет запрошен в консоли)
- После выполнения в корне появится (и будет удалён после загрузки) файл `info.json`
- В Яндекс.Диске будет создана папка с названием города, внутри — `info.json`

## 🤝 Вклад в проект

Я всегда рад помощи!) Если вы хотите внести вклад в проект:

1. Форкните репозиторий
2. Создайте ветку для вашей функции: `git checkout -b feature/YourFeature`
3. Закоммитьте изменения: `git commit -m 'Add some YourFeature'`
4. Запушьте в ветку: `git push origin feature/YourFeature`
5. Откройте Pull Request

## 📄 Лицензия

Этот проект лицензирован по лицензии MIT — подробности см. в файле LICENSE.

## 👨‍💻 Автор

**Igor Gashenko**

- GitHub: [@igor4000-ai](https://github.com/igor4000-ai)
- GitVerse: [@igor4000](https://gitverse.ru/igor4000)
- PyPi: [@igor4000](https://pypi.org/user/igor4000/)
- Email: igor_4000@mail.ru


## 🙏 Благодарности

- [ipify](https://www.ipify.org/) — API для определения IP-адреса
- [ipinfo.io](https://ipinfo.io/) — API для геолокации по IP
- [Яндекс.Диск API](https://yandex.ru/dev/disk/) — API для работы с облачным хранилищем

## 📝 Изменения

### Версия 1.0.0
- Первая версия проекта: IP, город, интеграция с Яндекс.Диском, сохранение/удаление данных

---

⭐ Если проект оказался полезным, поддержите его звездой на GitHub!
