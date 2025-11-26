from __future__ import print_function
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Escopo de permissão: permite ler e editar sua planilha
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_credentials():
    """
    Realiza a autenticação com o Google.
    Usa o arquivo credentials.json (baixado do Google Cloud)
    e cria/atualiza automaticamente o token.json.
    """

    creds = None

    # Token salva a sessão para não precisar logar toda vez
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # Se não houver token ou estiver inválido → fazer login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Salva o token para uso futuro
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds
