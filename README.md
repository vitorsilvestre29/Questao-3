# 📋 To-Do CLI

Aplicação de linha de comando em Python para gerenciamento pessoal de tarefas. Sem dependências externas — apenas stdlib.

---

## Instalação e uso rápido

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/todo-cli.git
cd todo-cli

# Python 3.8+ — sem instalação de pacotes necessária
python todo.py add "Estudar Apache Iceberg"
python todo.py list
python todo.py toggle 1
```

---

## Comandos

### `add` — Adicionar tarefa

```bash
python todo.py add "Título da tarefa"
```

**Saída:**
```
✅ Tarefa #1 adicionada: "Estudar Apache Iceberg"
```

---

### `list` — Listar tarefas

```bash
python todo.py list              # todas
python todo.py list --pending    # apenas pendentes
python todo.py list --done       # apenas concluídas
```

**Saída:**
```
ID    Status   Criada em              Título
──────────────────────────────────────────────────────────────────────
#1    ✗ pendente  08/06/2026 14:30       Estudar Apache Iceberg
#2    ✓ feita     08/06/2026 14:31       Configurar Docker

1/2 concluída(s)
```

---

### `toggle` — Marcar/desmarcar como concluída

```bash
python todo.py toggle <id>
```

**Saída:**
```
Tarefa #1 marcada como concluída ✓: "Estudar Apache Iceberg"
```

Executar novamente inverte para pendente.

---

## Especificação

### Descrição

Aplicação CLI em Python para gerenciamento pessoal de tarefas. O usuário interage via subcomandos no terminal. Os dados persistem entre sessões em um arquivo JSON local (`tasks.json`), criado automaticamente na primeira execução.

---

### Regras de Negócio

| ID | Regra |
|---|---|
| **RN-01** | Cada tarefa recebe um ID inteiro único, sequencial e imutável, atribuído automaticamente na criação |
| **RN-02** | Campos obrigatórios: `id` (int), `title` (str, 1–200 chars), `done` (bool, default `false`), `created_at` (ISO 8601) |
| **RN-03** | Dados persistem em `tasks.json` no diretório de execução; o arquivo é criado automaticamente se não existir |
| **RN-04** | O comando `toggle` inverte o estado atual (`false → true` ou `true → false`) — sempre toggle, sem separação entre marcar e desmarcar |
| **RN-05** | Título vazio ou composto só de espaços é rejeitado com mensagem de erro e exit code 1 |
| **RN-06** | Operações em IDs inexistentes retornam mensagem de erro e exit code 1 |

---

### Critérios de Aceite

| ID | Critério | Status |
|---|---|---|
| CA-01 | `add` com título válido persiste a tarefa e exibe confirmação com o ID gerado | ✅ |
| CA-02 | `add` com título vazio exibe erro e não cria tarefa | ✅ |
| CA-03 | `list` sem tarefas exibe "Nenhuma tarefa encontrada" | ✅ |
| CA-04 | `list` exibe ID, status (✓/✗), data de criação formatada e título | ✅ |
| CA-05 | `toggle` em ID existente inverte o status e confirma a mudança | ✅ |
| CA-06 | `toggle` em ID inexistente exibe erro e retorna exit code 1 | ✅ |
| CA-07 | O arquivo `tasks.json` é criado automaticamente se não existir | ✅ |
| CA-08 | IDs são únicos e não reutilizados (next_id sempre incrementa) | ✅ |

---

### Modelo de dados (`tasks.json`)

```json
{
  "next_id": 3,
  "tasks": [
    {
      "id": 1,
      "title": "Estudar Apache Iceberg",
      "done": true,
      "created_at": "2026-06-08T14:30:00"
    },
    {
      "id": 2,
      "title": "Configurar Docker",
      "done": false,
      "created_at": "2026-06-08T14:31:00"
    }
  ]
}
```

---

### Decisões de design

**Por que JSON e não SQLite?**  
JSON é legível, sem dependências e suficiente para o escopo. SQLite seria mais adequado se houvesse necessidade de buscas complexas ou múltiplos usuários simultâneos.

**Por que toggle em vez de `done` e `undone` separados?**  
Reduz a superfície da CLI. O estado atual é sempre visível via `list`, então o usuário sabe o que a operação vai fazer antes de executar.

**Por que `next_id` no JSON e não `max(id) + 1`?**  
Evita reutilização de IDs após uma eventual remoção futura de tarefas — o ID permanece imutável como identificador histórico.

---

## Estrutura do projeto

```
todo-cli/
├── todo.py        # Aplicação principal
├── tasks.json     # Gerado automaticamente (não versionar)
├── .gitignore
└── README.md
```

---

## Requisitos

- Python 3.8+
- Sem dependências externas

---

## Licença

MIT