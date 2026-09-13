# NetWatch

NetWatch é uma ferramenta de linha de comando para monitoramento de dispositivos de rede, desenvolvida em Python.

O projeto surgiu a partir do interesse por suporte técnico, infraestrutura e automação — identificar rapidamente se um equipamento está acessível ajuda no diagnóstico inicial de incidentes de rede.

## Funcionalidades

- Verificação de conectividade via ping
- Monitoramento de múltiplos dispositivos
- Identificação de status online/offline
- Registro de logs de cada verificação
- Detecção e registro de mudança de status (alertas)
- Leitura e cadastro de dispositivos via JSON
- Monitoramento contínuo com intervalo configurável
- Tratamento de erros (arquivo ausente ou JSON inválido)
- Resumo do ambiente ao final da execução

## Tecnologias

- Python 3
- subprocess
- JSON
- datetime

## Como executar

```bash
python netwatch.py
```

O menu permite executar uma verificação única, listar dispositivos, cadastrar novos dispositivos ou iniciar o monitoramento contínuo.

## Estrutura

```
netwatch/
├── netwatch.py
├── dispositivos.json
├── logs/
└── README.md
```

## Aprendizados

Durante o desenvolvimento foram praticados funções, listas, dicionários, leitura e escrita de arquivos, JSON, tratamento de exceções, execução de comandos do sistema operacional e lógica aplicada a monitoramento de rede.

## Próximos passos

Criar interface gráfica, monitoramento contínuo em segundo plano e notificações quando houver mudança de status.

> Dados e endereços utilizados neste repositório são fictícios, apenas para demonstração.
