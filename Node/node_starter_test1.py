import os
import sys
import subprocess
import platform
from pathlib import Path


def ask_question(question):
    answer = input(f"{question} (y/n): ").strip().lower()
    return answer == 'y'


def create_virtualenv(env_path):
    if not Path(env_path).exists():
        print(f"Создание виртуальной среды в {env_path}...")
        subprocess.check_call([sys.executable, "-m", "venv", env_path])
    else:
        print(f"Виртуальная среда уже существует в {env_path}")


def install_requirements(env_path):
    requirements_file = 'requirements.txt'
    if not Path(requirements_file).exists():
        print(f"Файл {requirements_file} не найден. Вам нужно создать его с зависимостями.")
        return

    print(f"Установка зависимостей из {requirements_file}...")
    pip_path = Path(env_path) / 'bin' / 'pip' if platform.system() != "Windows" else Path(env_path) / 'Scripts' / 'pip'
    subprocess.check_call([str(pip_path), "install", "-r", requirements_file])


def setup_system_service():
    if platform.system() != "Linux":
        print("Создание systemd-сервиса поддерживается только на Linux.")
        return

    service_name = 'monitoring.service'
    service_path = f'/etc/systemd/system/{service_name}'

    if Path(service_path).exists():
        print(f"Сервис {service_name} уже существует.")
        return

    print(f"Создание systemd сервиса {service_name}...")
    with open(service_path, 'w') as service_file:
        service_file.write("""[Unit]
Description=Monitoring Agent Service
After=network.target

[Service]
ExecStart=/path/to/your/venv/bin/python /path/to/your_script.py
WorkingDirectory=/path/to/your
Restart=always
User=your_username
Environment="PATH=/path/to/your/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

[Install]
WantedBy=multi-user.target
""")
    print(f"Сервис {service_name} создан. Не забудьте изменить путь и пользователя в файле.")
    if ask_question("Хотите активировать сервис и включить автозапуск?"):
        subprocess.check_call(["sudo", "systemctl", "daemon-reload"])
        subprocess.check_call(["sudo", "systemctl", "enable", service_name])
        subprocess.check_call(["sudo", "systemctl", "start", service_name])
        print(f"Сервис {service_name} активирован и запущен.")


def install_dependencies():
    if ask_question("Хотите создать виртуальную среду и установить зависимости?"):
        env_path = "venv"  # Путь для виртуальной среды
        create_virtualenv(env_path)
        install_requirements(env_path)


def install_and_run_node():
    if ask_question("Хотите запустить ноду?"):
        subprocess.check_call(["python", "your_script.py"])


def main():
    print("Привет! Это скрипт для настройки мониторинга сервера.")
    if ask_question("Хотите установить и запустить зависимости?"):
        install_dependencies()

    if ask_question("Хотите настроить и запустить системный сервис?"):
        setup_system_service()

    if ask_question("Хотите запустить ноду прямо сейчас?"):
        install_and_run_node()


if __name__ == "__main__":
    main()
