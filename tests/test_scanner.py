import argparse
import json
import socket
import tempfile
import threading
import unittest
from pathlib import Path

from scanner import ler_portas, salvar_resultados, testar_porta


class TestesDoScanner(unittest.TestCase):
    def test_ler_portas(self):
        self.assertEqual(ler_portas("80,22,8000-8002"), [22, 80, 8000, 8001, 8002])
        with self.assertRaises(argparse.ArgumentTypeError):
            ler_portas("porta")

    def test_porta_local_aberta_e_banner(self):
        servidor = socket.socket()
        servidor.bind(("127.0.0.1", 0))
        servidor.listen(1)
        porta = servidor.getsockname()[1]

        def responder():
            cliente, _ = servidor.accept()
            cliente.sendall(b"Ola do servidor")
            cliente.close()
            servidor.close()

        thread = threading.Thread(target=responder)
        thread.start()
        resultado = testar_porta("127.0.0.1", porta, 1, True)
        thread.join()

        self.assertEqual(resultado["estado"], "aberta")
        self.assertEqual(resultado["banner"], "Ola do servidor")

    def test_salvar_json(self):
        resultados = [{"porta": 80, "estado": "aberta", "banner": "teste"}]
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / "resultado.json"
            salvar_resultados(resultados, str(arquivo))
            salvo = json.loads(arquivo.read_text(encoding="utf-8"))
        self.assertEqual(salvo, resultados)


if __name__ == "__main__":
    unittest.main()

