# Voz do Povo - Backend

Este é o backend para o projeto Voz do Povo, uma plataforma para conectar cidadãos e a gestão pública.

## O Que Foi Feito

1.  **Modelo de Usuário Customizado**: Foi implementado um modelo de usuário (`User`) customizado que herda do `AbstractUser` do Django. Isso permite maior flexibilidade para futuras modificações.
2.  **Gerenciador de Usuário**: Um `UserManager` customizado foi criado para gerenciar a criação de usuários e superusuários, utilizando `email` e `username` como campos principais.
3.  **Ajuste no Campo `username`**: O modelo `User` e seu gerenciador foram ajustados para resolver um `TypeError` que ocorria durante a criação de um superusuário. O campo `username` foi definido como o campo de login (`USERNAME_FIELD`).
4.  **Estrutura de Autenticação**: Foram criadas as rotas e views básicas para registro (`/api/auth/register/`) e login (`/api/auth/login/`) de usuários usando `djangorestframework-simplejwt` para autenticação baseada em token.
5.  **API de Localidades**: Foi criada a API para consulta de estados e cidades, com rotas em `/api/localidades/`. Os dados de estados são populados via migração e os de cidades através de um comando customizado que consome a API do IBGE.

## Como Rodar o Projeto

1.  **Clone o Repositório** (se ainda não o fez).

2.  **Crie e Ative um Ambiente Virtual**:
    ```bash
    # Crie o ambiente virtual
    python -m venv .venv

    # Ative no Windows
    .\.venv\Scripts\activate

    # Ative no Linux/macOS
    # source .venv/bin/activate
    ```

3.  **Instale as Dependências**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute as Migrações do Banco de Dados**:
    ```bash
    python manage.py migrate
    ```

5.  **Popule o Banco de Dados com Localidades**:
    Execute os comandos abaixo para popular o banco de dados com os estados e cidades do Brasil.
    ```bash
    # Popula os estados (executa a migração de dados)
    python manage.py migrate localidades

    # Popula as cidades (executa o comando customizado)
    python manage.py populate_cities
    ```

6.  **Crie um Superusuário** (para acesso ao Admin):
    ```bash
    python manage.py createsuperuser
    ```
    Siga as instruções no terminal para definir `username`, `email` e `password`.

6.  **Inicie o Servidor de Desenvolvimento**:
    ```bash
    python manage.py runserver
    ```
    O servidor estará disponível em `http://127.0.0.1:8000/`.

## Rotas da API

Aqui estão as rotas de autenticação disponíveis e como interagir com elas.

---

### Registro de Usuário

-   **Endpoint**: `POST /api/auth/register/`
-   **Descrição**: Cria um novo usuário no sistema.
-   **Body (raw/json)**:
    ```json
    {
        "username": "seu_username",
        "email": "seu_email@exemplo.com",
        "password": "sua_senha_forte",
        "first_name": "Seu Nome"
    }
    ```
-   **Resposta de Sucesso (201 Created)**:
    ```json
    {
        "id": 1,
        "username": "seu_username",
        "email": "seu_email@exemplo.com",
        "first_name": "Seu Nome"
    }
    ```

---

### Login de Usuário

-   **Endpoint**: `POST /api/auth/login/`
-   **Descrição**: Autentica um usuário e retorna um par de tokens JWT (acesso e atualização).
-   **Body (raw/json)**:
    ```json
    {
        "username": "seu_username",
        "password": "sua_senha_forte"
    }
    ```
-   **Resposta de Sucesso (200 OK)**:
    ```json
    {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```

---

### Atualizar Token de Acesso

-   **Endpoint**: `POST /api/auth/login/refresh/`
-   **Descrição**: Gera um novo token de acesso usando um token de atualização (`refresh token`) válido.
-   **Body (raw/json)**:
    ```json
    {
        "refresh": "seu_refresh_token_obtido_no_login"
    }
    ```
-   **Resposta de Sucesso (200 OK)**:
    ```json
    {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```

---

### Localidades (`/api/localidades/`)

-   `GET /api/localidades/estados/`: Retorna uma lista de todos os estados do Brasil.
-   `GET /api/localidades/estados/{id}/`: Retorna os detalhes de um estado específico.
-   `GET /api/localidades/cidades/`: Retorna uma lista de cidades. Pode ser filtrado por estado.
-   `GET /api/localidades/cidades/{id}/`: Retorna os detalhes de uma cidade específica.
