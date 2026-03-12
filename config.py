from typing import Dict, Any


class Config:
    """Класс с конфигурационными настройками приложения."""

    # API endpoints
    URL_IP: str = "https://api.ipify.org"
    BASE_URL_CITY: str = "https://ipinfo.io"
    URL_YD: str = "https://cloud-api.yandex.net"
    LINK_DL_FILE: str = "https://cloud-api.yandex.net/v1/disk/resources/upload"

    # Файловые настройки
    FILE_NAME: str = "info.json"

    # Настройки запросов
    REQUEST_TIMEOUT: int = 5  # секунды

    # Параметры для загрузки на Яндекс.Диск
    UPLOAD_PARAMS: Dict[str, Any] = {
        "path": FILE_NAME,
        "fields": "href",
        "overwrite": True,
    }
