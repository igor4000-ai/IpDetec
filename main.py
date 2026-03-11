"""
Программа для получения IP-адреса, информации о городе и загрузки
этих данных на Яндекс Диск.

Пример использования:
    if __name__ == '__main__':
        main()
"""

from core import IPInfoAPI, CityInfoAPI, FileManager, YandexDiskUploader


def main() -> None:
    """
    Основная функция программы.

    Выполняет следующие действия:
    1. Получает IP-адрес пользователя
    2. Получает информацию о городе
    3. Сохраняет данные в JSON-файл
    4. Загружает файл на Яндекс.Диск
    5. Удаляет локальный файл
    """
    try:
        # Инициализируем API и менеджеры
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
        print(f"Данные сохранены в файл: {file_manager.file_name}")

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
