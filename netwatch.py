import subprocess
import platform
import json
import time

from datetime import datetime

ARQUIVO_DISPOSITIVOS = "dispositivos.json"
ARQUIVO_LOG = "logs/netwatch.log"
ARQUIVO_EVENTOS = "logs/eventos.log"

status_anterior = {}


def carregar_dispositivos():
    try:
        with open(ARQUIVO_DISPOSITIVOS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    except FileNotFoundError:
        print("Arquivo dispositivos.json não encontrado.")
        return []

    except json.JSONDecodeError:
        print("Erro ao ler dispositivos.json.")
        return []


def salvar_dispositivos(dispositivos):
    with open(ARQUIVO_DISPOSITIVOS, "w", encoding="utf-8") as arquivo:
        json.dump(dispositivos, arquivo, indent=4, ensure_ascii=False)


def verificar_dispositivo(ip):
    sistema = platform.system().lower()
    parametro = "-n" if sistema == "windows" else "-c"

    resultado = subprocess.run(
        ["ping", parametro, "1", ip],
        capture_output=True,
        text=True
    )

    return resultado.returncode == 0


def registrar_log(nome, ip, status):
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    linha = f"{agora} | {nome} | {ip} | {status}\n"

    with open(ARQUIVO_LOG, "a", encoding="utf-8") as arquivo:
        arquivo.write(linha)


def registrar_evento(nome, status_antigo, status_novo):
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    linha = f"{agora} | {nome} | {status_antigo} -> {status_novo}\n"

    with open(ARQUIVO_EVENTOS, "a", encoding="utf-8") as arquivo:
        arquivo.write(linha)


def executar_monitoramento():
    dispositivos = carregar_dispositivos()

    if not dispositivos:
        print("Nenhum dispositivo cadastrado.")
        return

    online = 0
    offline = 0
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    print("=" * 50)
    print("          NETWATCH")
    print("=" * 50)
    print("\nMonitor de Infraestrutura\n")
    print(agora)
    print()
    print(f"{'Dispositivo':<23}{'IP':<17}{'Status'}")
    print("-" * 50)

    for dispositivo in dispositivos:
        nome = dispositivo["nome"]
        ip = dispositivo["ip"]

        status_online = verificar_dispositivo(ip)
        status = "ONLINE" if status_online else "OFFLINE"

        if status_online:
            online += 1
        else:
            offline += 1

        print(f"{nome:<23}{ip:<17}{status}")

        registrar_log(nome, ip, status)

        if nome in status_anterior and status_anterior[nome] != status:
            print(f"\nALERTA: {nome} mudou de {status_anterior[nome]} para {status}\n")
            registrar_evento(nome, status_anterior[nome], status)

        status_anterior[nome] = status

    total = online + offline

    print("-" * 50)
    print("\nResumo\n")
    print(f"Online: {online}")
    print(f"Offline: {offline}")
    print(f"Total: {total}")


def mostrar_dispositivos():
    dispositivos = carregar_dispositivos()

    if not dispositivos:
        print("Nenhum dispositivo cadastrado.")
        return

    print()
    for dispositivo in dispositivos:
        print(dispositivo["nome"], "-", dispositivo["ip"])


def adicionar_dispositivo():
    nome = input("Nome do dispositivo: ").strip()
    ip = input("IP do dispositivo: ").strip()

    if not nome or not ip:
        print("Nome e IP são obrigatórios.")
        return

    dispositivos = carregar_dispositivos()
    dispositivos.append({"nome": nome, "ip": ip})
    salvar_dispositivos(dispositivos)

    print(f"Dispositivo '{nome}' adicionado.")


def monitoramento_continuo():
    try:
        intervalo = int(input("Intervalo entre verificações em segundos: "))
    except ValueError:
        print("Valor inválido.")
        return

    print("\nPressione Ctrl+C para interromper.\n")

    try:
        while True:
            executar_monitoramento()
            print(f"\nNova verificação em {intervalo} segundos...\n")
            time.sleep(intervalo)
    except KeyboardInterrupt:
        print("\nMonitoramento interrompido.")


def menu():
    while True:
        print("\nNETWATCH")
        print("1 - Executar verificação")
        print("2 - Mostrar dispositivos")
        print("3 - Adicionar dispositivo")
        print("4 - Monitoramento contínuo")
        print("5 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            executar_monitoramento()
        elif opcao == "2":
            mostrar_dispositivos()
        elif opcao == "3":
            adicionar_dispositivo()
        elif opcao == "4":
            monitoramento_continuo()
        elif opcao == "5":
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
