import requests
import random
import time
import logging
from cars.models import AuctionCars


user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
]


def fetch_data_from_api(url, page, sessionid):
    try:
        headers = {
            'User-Agent': random.choice(user_agents),
            'Cookie': f'sessionid={sessionid}'
        }

        params = {
            'page': page,
            'type': 'auction',
            'is_subscribed': 'false',
            'is_retried': 'false',
            'is_previously_bid': 'false',
            'order': 'default'
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            if not data:
                return None, True, True
            return data, False, True
        elif response.status_code == 401:
            logging.error("Ошибка 401: Неавторизованный доступ. Завершаем выполнение.")
            return None, False, False
        else:
            logging.error(f"Ошибка запроса: {response.status_code} на странице {page}")
            return None, True, True
    except Exception as e:
        logging.exception(f"Ошибка при запросе к API на странице {page}: {e}")
        return None, True, True


def fetch_car_card(car_id, sessionid):
    url = f"https://api.heydealer.com/v2/dealers/web/cars/{car_id}/"

    headers = {
        'User-Agent': random.choice(user_agents),
        'Cookie': f'sessionid={sessionid}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get('detail', ''), True
    elif response.status_code == 401:
        logging.error("Ошибка 401: Неавторизованный доступ. Завершаем выполнение.")
        return None, False
    else:
        logging.error(f"Ошибка запроса: {response.status_code} на странице")
        return None, True


def parse_params(data, sessionid):
    try:
        id_car = data.get("hash_id", '')
        if id_car:
            details_car, is_login = fetch_car_card(id_car, sessionid)

            if not is_login:
                return False

            if details_car:
                brand = details_car.get('brand_name', '')
                model = details_car.get('model_part_name', '')
                grade = details_car.get('grade_part_name', '')
                year = details_car.get('year', 0)
                fuel = details_car.get('fuel_display', '')
                transmission = details_car.get('transmission', '')
                color = details_car.get('color', '')
                mileage = details_car.get('mileage', 0)

                photos = details_car.get('image_urls', [])
                if photos:
                    image_urls_str = ",".join(photos)
                else:
                    image_urls_str = ''

                AuctionCars.objects.update_or_create(api_id=id_car, defaults={
                    'brand': brand,
                    'model': model,
                    'grade': grade,
                    'year': year,
                    'fuel': fuel,
                    'transmission': transmission,
                    'color': color,
                    'mileage': mileage,
                    'photos': image_urls_str
                })

                return True

    except Exception as e:
        logging.exception(f"Ошибка обработки данных: {e}")
        return True


def fetch_login():
    url = "https://api.heydealer.com/v2/dealers/web/login/"
    data = {
        "username": "sewa2020",
        "password": "Sewa20201!",
        "device_type": "pc"
    }

    response = requests.post(url, json=data)
    if response.status_code == 200:
        sessionid = response.cookies.get("sessionid")
        return sessionid
    else:
        logging.error(f"Ошибка запроса: {response.status_code} при авторизации")
        return None


def main():
    url = "https://api.heydealer.com/v2/dealers/web/cars/"
    sessionid = fetch_login()

    if sessionid:

        page = 1
        while True:
            try:
                data, is_empty, is_login = fetch_data_from_api(url, page, sessionid)

                if is_empty:
                    logging.info(f"Данные отсутствуют на странице {page}. Завершаем выполнение.")
                    break

                if not is_login:
                    sessionid = fetch_login()

                    page += 1
                    continue

                if not data:
                    page += 1
                    continue

                for data_elem in data:
                    success = parse_params(data_elem, sessionid)

                    if not success:
                        sessionid = fetch_login()

                    delay = random.randint(10, 15)
                    time.sleep(delay)

                delay = random.randint(10, 15)
                time.sleep(delay)

                page += 1
            except Exception as e:
                logging.exception(f"Ошибка в основном цикле на странице {page}: {e}")
                break
    else:
        logging.error('Завершаем парсинг')
