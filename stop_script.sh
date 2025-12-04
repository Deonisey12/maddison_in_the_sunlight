#!/bin/bash

PID_FILE="bot.pid"

if [ ! -f "$PID_FILE" ]; then
    echo "PID файл не найден. Процесс, возможно, не запущен."
    exit 1
fi

PID=$(cat "$PID_FILE")

if ! ps -p "$PID" > /dev/null 2>&1; then
    echo "Процесс с PID $PID не найден. Удаляю устаревший PID файл."
    rm -f "$PID_FILE"
    exit 1
fi

echo "Останавливаю процесс (PID: $PID)..."
kill "$PID"

for i in {1..10}; do
    if ! ps -p "$PID" > /dev/null 2>&1; then
        echo "Процесс успешно остановлен"
        rm -f "$PID_FILE"
        exit 0
    fi
    sleep 1
done

echo "Процесс не остановился за 10 секунд. Принудительная остановка..."
kill -9 "$PID" 2>/dev/null
rm -f "$PID_FILE"
echo "Процесс принудительно остановлен"

