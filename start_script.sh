#!/bin/bash

PID_FILE="bot.pid"
LOG_FILE="output.log"

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

source venv/bin/activate
nohup python3 src/__main__.py > "$LOG_FILE" 2>&1 &
NEW_PID=$!

echo "$NEW_PID" > "$PID_FILE"
echo "Процесс запущен (PID: $NEW_PID)"
echo "Для остановки используйте: ./stop_script.sh"