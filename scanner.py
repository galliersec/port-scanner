"""Scanner de portas simples para estudar Python e redes."""

import argparse
import csv
import json
import socket


def ler_portas(texto):
    """Converte '22,80,8000-8002' em [22, 80, 8000, 8001, 8002]."""
    portas = []
    try:
        for parte in texto.split(","):
            if "-" in parte:
                inicio, fim = parte.split("-")
                portas.extend(range(int(inicio), int(fim) + 1))
            else:
                portas.append(int(parte))
    except ValueError:
        raise argparse.ArgumentTypeError("Use assim: 22,80,8000-8002")

    if not portas or any(porta < 1 or porta > 65535 for porta in portas):
        raise argparse.ArgumentTypeError("As portas devem estar entre 1 e 65535")
    return sorted(set(portas))


def testar_porta(ip, porta, timeout, pegar_banner):
    """Tenta conectar a uma porta e devolve o resultado."""
    resultado = {"porta": porta, "estado": "fechada", "banner": ""}

    # AF_INET significa IPv4. SOCK_STREAM significa TCP.
    conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conexao.settimeout(timeout)

    try:
        conexao.connect((ip, porta))
        resultado["estado"] = "aberta"

        if pegar_banner:
            try:
                dados = conexao.recv(1024)
                resultado["banner"] = dados.decode("utf-8", errors="replace").strip()
            except socket.timeout:
                # Muitos serviços esperam uma mensagem antes de responder.
                resultado["banner"] = "sem banner"
    except socket.timeout:
        resultado["estado"] = "timeout"
    except OSError:
        resultado["estado"] = "fechada"
    finally:
        conexao.close()

    return resultado


def salvar_resultados(resultados, arquivo):
    """Salva os resultados em JSON ou CSV."""
    if arquivo.endswith(".json"):
        with open(arquivo, "w", encoding="utf-8") as saida:
            json.dump(resultados, saida, indent=2, ensure_ascii=False)
    elif arquivo.endswith(".csv"):
        with open(arquivo, "w", encoding="utf-8", newline="") as saida:
            escritor = csv.DictWriter(saida, fieldnames=["porta", "estado", "banner"])
            escritor.writeheader()
            escritor.writerows(resultados)
    else:
        raise ValueError("O arquivo precisa terminar em .json ou .csv")


def main():
    parser = argparse.ArgumentParser(description="Scanner TCP simples")
    parser.add_argument("alvo", help="IP ou site, por exemplo: 127.0.0.1")
    parser.add_argument("-p", "--portas", type=ler_portas, default=ler_portas("22,80,443"))
    parser.add_argument("-t", "--timeout", type=float, default=0.5)
    parser.add_argument("--banner", action="store_true")
    parser.add_argument("-o", "--output", help="Resultado .json ou .csv")
    args = parser.parse_args()

    try:
        ip = socket.gethostbyname(args.alvo)
    except socket.gaierror:
        parser.error("Não foi possível encontrar o alvo")

    resultados = []
    print(f"Escaneando {args.alvo} ({ip})...")

    for porta in args.portas:
        resultado = testar_porta(ip, porta, args.timeout, args.banner)
        resultados.append(resultado)
        print(f"Porta {porta}: {resultado['estado']} | {resultado['banner']}")

    if args.output:
        try:
            salvar_resultados(resultados, args.output)
            print(f"Resultado salvo em {args.output}")
        except ValueError as erro:
            parser.error(str(erro))


if __name__ == "__main__":
    main()

