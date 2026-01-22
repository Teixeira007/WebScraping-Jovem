# Monitor de Passagens ID Jovem - Guanabara

Este projeto monitora automaticamente a disponibilidade de passagens com benefício ID Jovem (100% ou 50% de desconto) no site da Viação Guanabara.

## Como usar localmente

1.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Execute o monitor:**
    Você precisa passar as datas de início e fim da busca, além das chaves do Telegram se quiser notificações.
    ```bash
    python main.py --start 2026-02-15 --end 2026-03-15 --telegram-token "SEU_TOKEN" --telegram-chat-id "SEU_CHAT_ID"
    ```

    **Argumentos opcionais:**
    *   `--origin`: Cidade de origem (Padrão: "Joao Pessoa - PB")
    *   `--destination`: Cidade de destino (Padrão: "Irece - BA")
    *   `--interval`: Intervalo em minutos entre as checagens (Padrão: 15)
    *   `--once`: Roda apenas uma verificação e encerra (bom para testes ou cron jobs).

## Deploy no GitHub Actions (Gratuito)

Este projeto já está configurado para rodar automaticamente no GitHub Actions.

### Passos para configurar:

1.  Suba este código para um repositório no GitHub.
2.  Vá na aba **Settings** do repositório.
3.  No menu lateral, vá em **Secrets and variables** > **Actions**.
4.  Clique em **New repository secret** e adicione as seguintes chaves:
    *   `TELEGRAM_TOKEN`: Seu token do bot do Telegram.
    *   `TELEGRAM_CHAT_ID`: O ID do chat onde receberá as mensagens.

### Funcionamento:
*   O script está agendado (`.github/workflows/monitor.yml`) para rodar **a cada 12 horas** (09:00 e 21:00 UTC).
*   Você pode alterar o intervalo ditando o arquivo `.github/workflows/monitor.yml`.
