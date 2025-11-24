#!/bin/bash

# --- DETECTA AMBIENTE ---
BASE_DIR=$(pwd)

if [[ "$BASE_DIR" == *"teste"* ]]; then
    AMBIENTE="teste"
    SERVICE="gunicorn_teste"
else
    AMBIENTE="producao"
    SERVICE="gunicorn"
fi

echo "============================================================="
echo "🛠  Iniciando deploy no ambiente: $AMBIENTE"
echo "🛠  Serviço Gunicorn alvo: $SERVICE"
echo "============================================================="

# --- LOG ---
LOG_FILE="$BASE_DIR/deploy.log"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Início do deploy ($AMBIENTE)" >> $LOG_FILE

# --- ATUALIZAR CÓDIGO ---
echo "→ Atualizando repositório..."
git pull >> $LOG_FILE 2>&1

# --- INSTALAR DEPENDÊNCIAS (opcional) ---
echo "→ Instalando dependências..."
pip install -r requirements.txt >> $LOG_FILE 2>&1

# --- MIGRAÇÕES ---
echo "→ Aplicando migrações..."
python3 manage.py makemigrations >> $LOG_FILE 2>&1
python3 manage.py migrate >> $LOG_FILE 2>&1

# --- STATICFILES ---
echo "→ Coletando staticfiles..."
python3 manage.py collectstatic --noinput >> $LOG_FILE 2>&1

# --- REINICIAR SERVIÇOS ---
echo "→ Reiniciando serviços..."
sudo systemctl restart $SERVICE
sudo systemctl restart nginx

echo "→ Deploy finalizado!"

# --- FINAL DO LOG ---
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Deploy concluído!" >> $LOG_FILE
echo "============================================================="
