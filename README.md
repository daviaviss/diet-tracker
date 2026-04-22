# diet-tracker

Aplicativo desktop para acompanhamento de dieta e hábitos alimentares, desenvolvido em Python com Tkinter.

## Funcionalidades

- Criar e acessar conta com autenticação segura (bcrypt)
- Registro de refeições com categorias e status de dieta
- Controle de atividades físicas
- Lembretes personalizados
- Cálculo de TMB e objetivo calórico
- Relatório de progresso com exportação em CSV

## Dependências

- **SQLAlchemy** — ORM e gerenciamento do banco de dados SQLite
- **bcrypt** — criptografia de senhas

## Como executar

### 1. Configure o ambiente virtual (opcional, mas recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Execute o programa

```bash
python main.py
```

## Arquitetura

O projeto segue o padrão **MVC + DAO**:

- **Model** — entidades mapeadas com SQLAlchemy, banco SQLite local
- **View** — frames Tkinter, sem lógica de negócio
- **Controller** — valida dados, aciona o DAO e dispara navegação
- **DAO** — único ponto de acesso ao banco, com gerenciamento de sessão via context manager
