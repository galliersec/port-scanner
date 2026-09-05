# Port Scanner em Python

Este é um scanner de portas simples, feito para aprender Python e entender como uma conexão TCP funciona. Você informa um endereço e algumas portas; o programa tenta se conectar e mostra quais responderam.

> Use o scanner somente no seu computador, nos seus equipamentos ou em ambientes onde você recebeu autorização.

## Teste rápido

Vamos testar tudo no seu próprio computador. Você precisará de dois terminais abertos na pasta do projeto:

```powershell
cd C:\Users\Admin\Downloads\projects\port-scanner
```

No primeiro terminal, crie um pequeno servidor na porta `8000`:

```powershell
python -m http.server 8000 --bind 127.0.0.1
```

Deixe esse terminal aberto. No segundo, execute o scanner:

```powershell
python scanner.py 127.0.0.1 -p 7998-8002
```

Você verá algo parecido com:

```text
Escaneando 127.0.0.1 (127.0.0.1)...
Porta 7998: fechada |
Porta 7999: fechada |
Porta 8000: aberta |
Porta 8001: fechada |
Porta 8002: fechada |
```

A porta `8000` aparece aberta porque o servidor está funcionando nela. As outras não possuem um serviço esperando conexões. Dependendo do firewall, elas também podem aparecer como `timeout`.

Volte ao primeiro terminal e pressione `Ctrl+C` para desligar o servidor. Execute o scanner novamente e observe o que acontece com a porta `8000`.

## Comandos úteis

Testar portas específicas:

```powershell
python scanner.py 127.0.0.1 -p 22,80,443
```

Testar um intervalo maior:

```powershell
python scanner.py 127.0.0.1 -p 7900-8100 -t 0.2
```

Tentar ler o banner enviado pelo serviço:

```powershell
python scanner.py 127.0.0.1 -p 8000 --banner
```

Salvar o resultado:

```powershell
python scanner.py 127.0.0.1 -p 7998-8002 -o resultado.json
python scanner.py 127.0.0.1 -p 7998-8002 -o resultado.csv
```

## O que cada opção significa

- `127.0.0.1`: representa o seu próprio computador.
- `-p`: escolhe as portas que serão testadas.
- `-t`: define quantos segundos o programa espera por uma resposta.
- `--banner`: tenta ler a mensagem inicial enviada pelo serviço.
- `-o`: salva o resultado em um arquivo JSON ou CSV.

## Como o programa descobre uma porta aberta?

O ponto principal está na função `testar_porta`, dentro de `scanner.py`:

```python
conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conexao.connect((ip, porta))
```

A primeira linha cria um socket TCP. Pense nele como um telefone que o programa usará para fazer uma ligação. A segunda linha tenta ligar para o endereço e a porta. Se a conexão acontecer, a porta está aberta.

O `timeout` limita o tempo dessa tentativa. Sem ele, o programa poderia ficar esperando por muito tempo quando um endereço não responde.

## Testes automáticos

Para conferir as funções do projeto:

```powershell
python -m unittest discover -s tests -v
```

Se aparecer `OK`, os testes passaram.

## Um exercício simples

Abra `scanner.py`, encontre esta linha:

```python
print(f"Escaneando {args.alvo} ({ip})...")
```

Troque a mensagem por outra de sua escolha, salve o arquivo e rode o scanner novamente. É uma pequena mudança, mas ajuda a praticar o ciclo mais importante da programação: editar, executar e observar o resultado.

