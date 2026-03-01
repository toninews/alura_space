# Alura Space

Aplicacao Django para cadastro e exibicao de fotografias do espaco. O projeto foi originalmente criado durante a formacao da Alura e agora foi ajustado para rodar localmente sem depender de S3.

## Stack

- Python 3.10+
- Django 4.1
- SQLite no desenvolvimento
- `django-storages` e `boto3` opcionais para uso com AWS S3

## Como rodar

1. Crie e ative um ambiente virtual.
2. Instale as dependencias:

```bash
pip install -r requirements.txt
```

3. Crie o arquivo `.env` com base no exemplo:

```bash
cp .env.example .env
```

4. Rode as migracoes:

```bash
python3 manage.py migrate
```

5. Inicie o servidor:

```bash
python3 manage.py runserver
```

## Variaveis de ambiente

- `SECRET_KEY`: chave secreta do Django
- `DEBUG`: `True` ou `False`
- `ALLOWED_HOSTS`: hosts separados por virgula
- `USE_S3`: `True` para habilitar upload e arquivos estaticos no S3
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_STORAGE_BUCKET_NAME`: necessarias apenas quando `USE_S3=True`

## Ajustes feitos

- Storage local como padrao para desenvolvimento
- Correcao da configuracao do Django e do guia de instalacao
- Protecao de rotas com autenticacao
- Associacao automatica da foto ao usuario autenticado
- Validacao de permissao para editar e deletar fotos
- Limpeza de templates com HTML invalido e exibicao de mensagens/erros

## Demo em video

O projeto inclui um video de demonstracao local em `video-demo/demo.mp4`.

## Publicacao no GitHub

Antes de publicar, vale revisar:

- nome do repositorio e descricao
- screenshots da aplicacao
- configuracao de producao (`DEBUG=False`, `ALLOWED_HOSTS`, S3 ou outro storage)
- secrets fora do repositorio
