#!/bin/bash

PID_FILE="bot.pid"
LOG_FILE="output.log"
VENV_DIR="venv"

if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "Процесс уже запущен (PID: $OLD_PID)"
        exit 1
    else
        echo "Удаляю устаревший PID файл"
        rm -f "$PID_FILE"
    fi
fi

# Проверка и создание виртуального окружения
if [ ! -d "$VENV_DIR" ]; then
    echo "Виртуальное окружение не найдено. Создаю новое..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "Ошибка при создании виртуального окружения"
        exit 1
    fi
    echo "Виртуальное окружение создано"
fi

# Активация виртуального окружения
source "$VENV_DIR/bin/activate"

# Обновление pip до последней версии
echo "Обновляю pip..."
pip install --upgrade pip --quiet

# Установка зависимостей проекта
echo "Устанавливаю зависимости проекта..."
pip install -e .
if [ $? -ne 0 ]; then
    echo "Ошибка при установке зависимостей"
    exit 1
fi

echo "Зависимости установлены. Запускаю бота..."

# Запуск бота
nohup python3 src/__main__.py > "$LOG_FILE" 2>&1 &
NEW_PID=$!

echo "$NEW_PID" > "$PID_FILE"
echo "Процесс запущен (PID: $NEW_PID)"
echo "Для остановки используйте: ./stop_script.sh"