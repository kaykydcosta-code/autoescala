from sheets import get_sheet, update_sheet, read_range
from datetime import datetime
import pytz

# -------------------------------
# CONFIGURAÇÕES DA SUA PLANILHA
# -------------------------------

SPREADSHEET_ID = "1hklEZUysvpX8ozx-nduy6541qTeWpA5VN60hHgYgpL4"
ABA_OPERACIONAL = "PLANILHA OPERACIONAL"
ABA_BACKUP = "BACKUP ONTEM"

# Intervalos — AJUSTE SE SUA PLANILHA TIVER ESTRUTURA DIFERENTE
INTERVALO_INDIVIDUAL = "A9:AK55"       # Onde ficam TODAS as escalas individuais
INTERVALO_GERAL = "A60:Z200"          # Onde fica a escala geral
INTERVALO_BACKUP = "A1:Z300"          # Onde será gravado o backup

# ---------------------------------------
# FUNÇÃO — Copia a escala de ontem (backup)
# ---------------------------------------

def fazer_backup():
    geral = read_range(SPREADSHEET_ID, ABA_OPERACIONAL, INTERVALO_GERAL)

    update_sheet(
        SPREADSHEET_ID,
        ABA_BACKUP,
        INTERVALO_BACKUP,
        geral
    )

    print("✔ Backup da escala geral realizado com sucesso!")

# -----------------------------------------------------------
# FUNÇÃO — Gera automaticamente a escala geral a partir das
# escalas individuais (a INDIVIDUAL é a FONTE DA VERDADE)
# -----------------------------------------------------------

def gerar_escala_geral():
    individuais = read_range(SPREADSHEET_ID, ABA_OPERACIONAL, INTERVALO_INDIVIDUAL)

    geral_processada = []

    for linha in individuais:
        if any(c.strip() for c in linha):  # Ignora linhas totalmente vazias
            geral_processada.append(linha)

    update_sheet(
        SPREADSHEET_ID,
        ABA_OPERACIONAL,
        INTERVALO_GERAL,
        geral_processada
    )

    print("✔ Escala geral atualizada automaticamente!")

# -------------------------------
# EXECUÇÃO PRINCIPAL DO SCRIPT
# -------------------------------

def main():
    tz = pytz.timezone("America/Sao_Paulo")
    hoje = datetime.now(tz)

    print("\n========== AUTOESCALA ==========\n")
    print("Data atual:", hoje.strftime("%d/%m/%Y %H:%M"))
    print("Executando sincronização...\n")

    fazer_backup()
    gerar_escala_geral()

    print("\n✔ Processo finalizado sem erros.")
    print("================================\n")


if __name__ == "__main__":
    main()
