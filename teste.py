from sheets import read_range

SPREADSHEET_ID = "1hklEZUysvpX8ozx-nduy6541qTeWpA5VN60hHgYgpL4"

print("Lendo ABA 2...")

dados = read_range(SPREADSHEET_ID, "PLANILHA OPERACIONAL!A1:D10")

print("Resultado:")
print(dados)
