import os
import sys
import subprocess
import platform
import shutil

NODE_SCRIPT_NAME = "node.py"
NODE_SERVICE_NAME = "monitoring.service"
VENV_DIR = "venv"


def ask_user(question):
    """Запрашивает у пользователя подтверждение (да/нет)"""
    answer = input(f"{question} [y/N]: ").strip().lower()
    return answer == "y"


def run_command(command, shell=False):
    """Выполняет команду в терминале"""
    try:
        subprocess.run(command, shell=shell, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка выполнения: {e}")
        sys.exit(1)


def install_virtualenv():
    """Создает виртуальное окружение и устанавливает зависимости"""
    if not ask_user("Создать виртуальное окружение и установить зависимости?"):
        return

    print("📦 Создаю виртуальное окружение...")
    run_command([sys.executable, "-m", "venv", VENV_DIR])

    pip_exec = os.path.join(VENV_DIR, "bin", "pip") if platform.system() != "Windows" else os.path.join(VENV_DIR,
                                                                                                        "Scripts",
                                                                                                        "pip.exe")

    print("📌 Устанавливаю зависимости...")
    run_command([pip_exec, "install", "psutil", "requests"])


def copy_node_script():
    """Копирует ноду в системную директорию"""
    if not ask_user("Скопировать скрипт ноды в системную директорию?"):
        return

    target_dir = "/opt/monitoring" if platform.system() != "Windows" else os.path.join(os.environ["ProgramFiles"],
                                                                                       "Monitoring")
    os.makedirs(target_dir, exist_ok=True)

    shutil.copy(NODE_SCRIPT_NAME, os.path.join(target_dir, NODE_SCRIPT_NAME))
    print(f"✅ Файл {NODE_SCRIPT_NAME} скопирован в {target_dir}")


def setup_systemd_service():
    """Настраивает systemd-сервис для автозапуска"""
    if platform.system() != "Linux":
        print("⚠️ Systemd доступен только в Linux. Пропускаю...")
        return

    if not ask_user("Создать и запустить systemd-сервис?"):
        return

    service_content = f"""[Unit]
Description=Monitoring Node Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/monitoring/{NODE_SCRIPT_NAME}
Restart=always
User={os.getlogin()}
WorkingDirectory=/opt/monitoring

[Install]
WantedBy=multi-user.target
"""

    service_path = f"/etc/systemd/system/{NODE_SERVICE_NAME}"

    with open(service_path, "w") as f:
        f.write(service_content)

    print(f"✅ Сервис systemd создан: {service_path}")

    print("🚀 Перезагружаю systemd...")
    run_command(["sudo", "systemctl", "daemon-reload"])

    print("🔄 Включаю автозапуск...")
    run_command(["sudo", "systemctl", "enable", NODE_SERVICE_NAME])

    print("▶️ Запускаю сервис...")
    run_command(["sudo", "systemctl", "start", NODE_SERVICE_NAME])

    print("✅ Сервис успешно запущен!")


def main():
    print("🔧 Установка ноды мониторинга серверов")

    install_virtualenv()
    copy_node_script()
    setup_systemd_service()

    print("🎉 Установка завершена!")


if __name__ == "__main__":
    main()
