#!/bin/bash

# Переход в директорию проекта
cd /mnt/c/Users/User/OneDrive/Рабочий стол/prod/Team-Project-12

# Установка Python предпоследней версии (пример: 3.12) если не установлен
if ! command -v python3.12 &> /dev/null; then
    echo "Python 3.12 не найден. Устанавливаю..."
    sudo apt update
    sudo apt install python3.12 python3.12-venv python3.12-distutils -y
fi

# Проверка наличия виртуального окружения
if [ ! -d "myenv" ]; then
    echo "Создаю виртуальное окружение на базе Python 3.12..."
    python3.12 -m venv myenv
fi

# Активация виртуального окружения
source myenv/bin/activate

# Обновление pip
pip install --upgrade pip

# Установка зависимостей
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "Зависимости установлены."
else
    echo "Файл requirements.txt не найден. Прекращаю выполнение."
    exit 1
fi

# Применение миграций
python manage.py migrate

# Запуск сервера Django на localhost, доступном по http://127.0.0.1:8000
python manage.py runserver 127.0.0.1:8000
