import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth import get_credentials


# =====================================================
#   CONECTA AO GOOGLE SHEETS
# =====================================================
def get_service():
    """
    Conecta ao Google Sheets usando as credenciais.
    Retorna o serviço pronto para ler/editar a planilha.
    """
    creds = get_credentials()
    service = build("sheets", "v4", credentials=creds)
    return service


# =====================================================
#   FUNÇÃO PARA LER UM INTERVALO
# =====================================================
def read_range(spreadsheet_id, range_name):
    """
    Lê um intervalo da planilha.
    """
    try:
        service = get_service()
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()
        return result.get("values", [])
    except HttpError as error:
        print(f"Erro ao ler intervalo: {error}")
        return None


# =====================================================
#   FUNÇÃO PARA ESCREVER EM UM INTERVALO
# =====================================================
def write_range(spreadsheet_id, range_name, values):
    """
    Escreve informações em um intervalo da planilha.
    """
    try:
        service = get_service()
        body = {"values": values}

        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()

        return result

    except HttpError as error:
        print(f"Erro ao escrever intervalo: {error}")
        return None


# =====================================================
#   COPIAR ESCALA DA ABA 2 PARA A ABA 3
# =====================================================
def copy_previous_scale(spreadsheet_id):
    """
    Copia toda a escala da aba 'PLANILHA OPERACIONAL'
    para a aba 'BACKUP ONTEM'
    antes das novas atualizações.

    Cobre colunas A até AZ e linhas 1 até 200.
    """

    source_range = "PLANILHA OPERACIONAL!A1:AZ200"
    destination_range = "BACKUP ONTEM!A1"

    try:
        service = get_service()

        # Ler dados da aba principal
        data = read_range(spreadsheet_id, source_range)
        if not data:
            print("Nenhum dado encontrado para copiar.")
            return None

        # Escrever na aba "BACKUP ONTEM"
        body = {"values": data}

        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=destination_range,
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()

        print("Backup criado com sucesso!")
        return result

    except HttpError as error:
        print(f"Erro ao copiar escala: {error}")
        return None
