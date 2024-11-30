#!/bin/bash

if [ ! -d ".venv" ]; then
    python -m venv .venv
    echo "Виртуальное окружение создано!"
fi

source .venv/Scripts/activate
pip install -r requirements.txt
echo "Зависимости проекта установлены!"