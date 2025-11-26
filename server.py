from fastapi import FastAPI
from sheets import read_range, write_range, copy_previous_scale

app = FastAPI()

SPREADSHEET_ID = "1hklEZUysvpX8ozx-nduy6541qTeWpA5VN60hHgYgpL4"

# Exemplo simples: testar conexão
@app.get("/")
def home():
    return {"status": "API rodando 👍"}

# Ler intervalo da planilha
@app.get("/ler")
def ler(range: str):
    dados = read_range(SPREADSHEET_ID, range)
    return {"resultado": dados}

# Escrever intervalo
@app.post("/escrever")
def escrever(range: str, valores: list[list[str]]):
    r = write_range(SPREADSHEET_ID, range, valores)
    return {"status": "ok", "detalhes": r}

# Backup da aba 2 para aba 3
@app.post("/backup")
def backup():
    copy_previous_scale(
        SPREADSHEET_ID,
        "PLANILHA OPERACIONAL!A1:AK200",
        "BACKUP ONTEM!A1:AK200"
    )
    return {"status": "backup feito"}

