"""
Модуль с основной логикой приложения:
- IPInfoAPI: получение текущего IP-адреса
- CityInfoAPI: получение информации о городе по IP
- FileManager: сохранение/удаление локального JSON-файла
- YandexDiskUploader: загрузка файла на Яндекс.Диск
"""

import json
import os
from typing import Any, Dict, Optional

import requests

from api_key import api_key_yd
from config import Config


class IPInfoAPI:
    """Класс для получения текущего IP-адреса."""

    def __init__(self, timeout: int = Config.REQUEST_TIMEOUT):
        """
        Инициализирует экземпляр класса IPInfoAPI.

        Args:
            timeout: Таймаут для HTTP запросов в секундах
        """
        self._timeout: int = timeout

    def get_ip(self) -> str:
        """
        Получает текущий IP-адрес.

        Returns:
            str: Текущий IP-адрес

        Raises:
            Exception: При ошибке получения IP-адреса
        """
        try:
            response = requests.get(Config.URL_IP, timeout=self._timeout)
            response.raise_for_status()
            ip = response.text.strip()

            if not ip:
                raise Exception("Получен пустой IP-адрес")

            print(f"IP-адрес успешно получен: {ip}")
            return ip
        except requests.Timeout as e:
            raise Exception(f"Таймаут при получении IP-адреса: {e}")
        except requests.RequestException as e:
            raise Exception(f"Ошибка сети при получении IP-адреса: {e}")


class CityInfoAPI:
    """Класс для получения информации о городе по IP-адресу."""

    def __init__(self, ip_api: IPInfoAPI, timeout: int = Config.REQUEST_TIMEOUT):
        """
        Инициализирует экземпляр класса CityInfoAPI.

        Args:
            ip_api: Экземпляр класса IPInfoAPI для получения IP-адреса
            timeout: Таймаут для HTTP запросов в секундах
        """
        self._ip_api = ip_api
        self._timeout: int = timeout
        self._ip: Optional[str] = None

    def get_city(self) -> str:
        """
        Получает название города по текущему IP-адресу.

        Returns:
            str: Название города

        Raises:
            Exception: При ошибке получения информации о городе
        """
        try:
            self._ip = self._ip_api.get_ip()
            response = requests.get(
                f"{Config.BASE_URL_CITY}/{self._ip}/geo",
                timeout=self._timeout,
            )
            response.raise_for_status()
            all_info = response.json()
            city = all_info.get("city", "Неизвестный город")
            print(f"Информация о городе успешно получена: {city}")
            return city
        except requests.Timeout as e:
            raise Exception(f"Таймаут при получении информации о городе: {e}")
        except requests.RequestException as e:
            raise Exception(f"Ошибка сети при получении информации о городе: {e}")

    def get_saved_ip(self) -> str:
        """
        Возвращает сохраненный IP-адрес.

        Returns:
            str: Сохраненный IP-адрес

        Raises:
            Exception: Если IP-адрес не был получен ранее
        """
        if self._ip is None:
            raise Exception(
                "IP-адрес не был получен. Сначала вызовите метод get_city()"
            )
        return self._ip


class FileManager:
    """Класс для управления локальными файлами."""

    def __init__(self, file_name: str = Config.FILE_NAME):
        """
        Инициализирует экземпляр класса FileManager.

        Args:
            file_name: Имя файла для работы
        """
        self._file_name: str = file_name

    def file_name(self) -> str:
        """
        Возвращает имя файла, с которым работает менеджер.

        Returns:
            str: Имя файла
        """
        return self._file_name

    def save_json(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Сохраняет данные в JSON-файл.

        Args:
            data: Словарь с данными для сохранения

        Returns:
            Dict[str, Any]: Сохраненные данные

        Raises:
            Exception: При ошибке сохранения файла
        """
        try:
            with open(self._file_name, "w", encoding="utf-8") as f:
                json_text = json.dumps(data, ensure_ascii=False, indent=2)
                f.write(json_text)
            return data

        except IOError as e:
            print(f"Ошибка при сохранении данных в файл: {e}")
            raise Exception(f"Ошибка ввода-вывода: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка при сохранении данных: {e}")
            raise Exception(f"Неожиданная ошибка: {e}")

    def remove_file(self) -> bool:
        """
        Удаляет локальный файл.

        Returns:
            bool: True если файл был успешно удален, False если файл не существовал

        Raises:
            Exception: При ошибке удаления файла
        """
        try:
            os.remove(self._file_name)
            print(f"Локальный файл {self._file_name} успешно удален")
            return True

        except FileNotFoundError:
            print(f"Файл {self._file_name} не найден")
            return False
        except Exception as e:
            print(f"Ошибка при удалении файла {self._file_name}: {e}")
            raise Exception(f"Ошибка удаления файла: {e}")


class YandexDiskUploader:
    """Класс для загрузки файлов на Яндекс.Диск."""

    def __init__(
        self,
        file_manager: FileManager,
        api_key: str = api_key_yd,
        timeout: int = Config.REQUEST_TIMEOUT,
    ):
        """
        Инициализирует экземпляр класса YandexDiskUploader.

        Args:
            file_manager: Экземпляр класса FileManager для работы с локальными файлами
            api_key: API-ключ для доступа к Яндекс.Диску
            timeout: Таймаут для HTTP запросов в секундах
        """
        self._file_manager: FileManager = file_manager
        self._api_key: str = api_key
        self._timeout: int = timeout
        self._headers: Dict[str, str] = {"Authorization": self._api_key}
        self._upload_params: Dict[str, Any] = Config.UPLOAD_PARAMS.copy()

    def _create_folder(self, folder_path: str) -> None:
        """
        Создает папку на Яндекс.Диске.

        Args:
            folder_path: Путь к папке на Яндекс.Диске

        Raises:
            Exception: При ошибке создания папки
        """
        try:
            response = requests.put(
                f"{Config.URL_YD}/v1/disk/resources",
                params={"path": folder_path},
                headers=self._headers,
                timeout=self._timeout,
            )
            # Папка может уже существовать, игнорируем ошибку 409
            if response.status_code not in (201, 409):
                response.raise_for_status()
            print(f"Папка {folder_path} готова для загрузки")
        except requests.Timeout as e:
            raise Exception(f"Таймаут при создании папки: {e}")
        except requests.RequestException as e:
            raise Exception(f"Ошибка сети при создании папки: {e}")

    def get_upload_link(self, city: Optional[str] = None) -> requests.Response:
        """
        Получает ссылку для загрузки файла на Яндекс.Диск.

        Args:
            city: Имя города для создания папки на Яндекс.Диске

        Returns:
            requests.Response: Ответ от API Яндекс.Диска с информацией о ссылке для загрузки

        Raises:
            Exception: При ошибке получения ссылки
        """
        try:
            # Формируем путь к файлу с учетом папки города
            params = self._upload_params.copy()
            if city:
                # Создаем папку перед загрузкой файла
                self._create_folder(city)
                params["path"] = f"{city}/{Config.FILE_NAME}"

            response = requests.get(
                Config.LINK_DL_FILE,
                params=params,
                headers=self._headers,
                timeout=self._timeout,
            )
            response.raise_for_status()
            print(f"Ссылка для загрузки успешно получена для пути: {params['path']}")
            return response
        except requests.Timeout as e:
            raise Exception(f"Таймаут при получении ссылки для загрузки: {e}")
        except requests.RequestException as e:
            raise Exception(f"Ошибка сети при получении ссылки для загрузки: {e}")

    def upload_file(self, city: Optional[str] = None) -> requests.Response:
        """
        Загружает файл на Яндекс.Диск.

        Args:
            city: Имя города для создания папки на Яндекс.Диске

        Returns:
            requests.Response: Ответ от API Яндекс.Диска с результатом загрузки

        Raises:
            Exception: При ошибке загрузки файла
        """
        try:
            # Получаем ссылку для загрузки
            link_response = self.get_upload_link(city)

            # Проверяем наличие ключа 'href' в ответе
            upload_url = link_response.json().get("href")
            if not upload_url:
                print("В ответе API отсутствует ссылка для загрузки (href)")
                raise Exception("Отсутствует ссылка для загрузки")

            # Открываем сохранённый JSON-файл в бинарном режиме и отправляем его содержимое
            with open(self._file_manager.file_name(), "rb") as f:
                response = requests.put(
                    upload_url,
                    data=f.read(),
                    headers={"Content-Type": "application/json; charset=utf-8"},
                    timeout=self._timeout,
                )
            response.raise_for_status()

            print(
                f"Файл успешно загружен на Яндекс.Диск. Статус: {response.status_code}"
            )
            return response
        except requests.Timeout as e:
            raise Exception(f"Таймаут при загрузке файла на Яндекс.Диск: {e}")
        except requests.RequestException as e:
            raise Exception(f"Ошибка сети при загрузке файла на Яндекс.Диск: {e}")
