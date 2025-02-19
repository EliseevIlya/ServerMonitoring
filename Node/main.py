import psutil
import requests
import platform
import time
import json

# URL вашего бэкенда, принимающего метрики
BACKEND_URL = "http://your-backend-url/api/metrics"

# Если требуется аутентификация, можно добавить API-ключ или токен
API_KEY = "your_api_key"  # Оставьте пустым, если не требуется


def get_server_metrics():
    """
    Собирает данные о сервере: информацию об ОС, загрузке CPU, использовании памяти,
    дисковой подсистеме и сетевой активности.
    """
    metrics = {}

    # Информация об ОС
    metrics['platform'] = platform.system()
    metrics['platform_release'] = platform.release()
    metrics['platform_version'] = platform.version()
    metrics['architecture'] = platform.machine()
    metrics['hostname'] = platform.node()

    # CPU
    # cpu_percent с интервалом в 1 секунду для более точного измерения
    metrics['cpu_usage'] = psutil.cpu_percent(interval=1)

    # Память
    metrics['memory'] = psutil.virtual_memory()._asdict()

    # Диски: собираем данные для каждого раздела
    disk_data = {}
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_data[partition.device] = usage._asdict()
        except Exception as e:
            # Возможны ошибки доступа для некоторых разделов
            disk_data[partition.device] = {"error": str(e)}
    metrics['disk'] = disk_data

    # Сетевая активность
    metrics['network'] = psutil.net_io_counters()._asdict()

    return metrics


def send_metrics(metrics):
    """
    Отправляет собранные метрики на бэкенд через HTTP POST.
    """
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"

    try:
        response = requests.post(BACKEND_URL, headers=headers, data=json.dumps(metrics))
        if response.status_code == 200:
            print("Метрики успешно отправлены")
        else:
            print(f"Ошибка отправки метрик, статус код: {response.status_code}")
    except Exception as e:
        print("Ошибка при отправке метрик:", e)


def main():
    # Период отправки метрик в секундах (например, каждые 60 секунд)
    interval = 60
    while True:
        metrics = get_server_metrics()
        print("Собранные метрики:", json.dumps(metrics, indent=2))
        send_metrics(metrics)
        time.sleep(interval)


if __name__ == "__main__":
    main()
