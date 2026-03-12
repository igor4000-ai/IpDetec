"""
Модуль main.py - точка входа в приложение IpDetec.

Этот модуль содержит основную функцию программы, которая выполняет:
- Получение IP-адреса пользователя
- Определение города по IP-адресу
- Сохранение данных в JSON-файл
- Загрузку файла на Яндекс.Диск
- Удаление локального файла после успешной загрузки

Пример использования:
    if __name__ == '__main__':
        main()
"""

from core import IPInfoAPI, CityInfoAPI, FileManager, YandexDiskUploader


def main() -> None:
    """
    Основная функция программы.

    Выполняет следующие действия:
    1. Инициализирует API и менеджер файлов
    2. Получает IP-адрес пользователя
    3. Получает информацию о городе
    4. Сохраняет данные в JSON-файл
    5. Загружает файл на Яндекс.Диск
    6. Удаляет локальный файл после успешной загрузки
    7. Выводит информацию о IP-адресе и городе

    Raises:
        Exception: При возникновении любой ошибки в процессе выполнения
    """
    try:
        # Инициализируем API и менеджер
        ip_api = IPInfoAPI()
        city_api = CityInfoAPI(ip_api)
        file_manager = FileManager()
        yandex_uploader = YandexDiskUploader(file_manager)

        # Получаем информацию о городе и IP-адрес
        city = city_api.get_city()

        # Получаем сохраненный IP-адрес из city_api
        ip = city_api.get_saved_ip()

        # Формируем данные для сохранения
        ip_city_data = {
            "ip": ip,
            "city": city,
        }

        # Сохраняем данные в файл
        file_manager.save_json(ip_city_data)
        print(f"Данные сохранены в файл: {file_manager.file_name()}")

        # Загружаем файл на Яндекс.Диск в папку с именем города
        upload_response = yandex_uploader.upload_file(city)

        # Удаляем локальный файл после успешной загрузки
        if upload_response.status_code in (200, 201):
            file_manager.remove_file()
        else:
            print("Ошибка при загрузке файла на Яндекс.Диск")

        # Выводим информацию о IP-адресе и городе
        print(f"Ваш IP-адрес: {ip}")
        print(f"Ваш город: {city}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
