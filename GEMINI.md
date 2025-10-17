# Gemini - Voz do Povo Backend

Este arquivo fornece um resumo do projeto e instruções para desenvolvimento.

## Visão Geral do Projeto

O "Voz do Povo" é uma plataforma backend construída com Django e Django Rest Framework. O objetivo é conectar cidadãos com a gestão pública, permitindo o envio de denúncias e o acesso a informações sobre localidades.

## Estrutura do Projeto

O projeto está organizado em várias aplicações Django:

-   `voz_do_povo`: O projeto principal do Django.
-   `applications/core`: Contém o modelo de usuário customizado.
-   `applications/autenticacao`: Gerencia a autenticação de usuários via JWT.
-   `applications/localidades`: Fornece a API para consulta de estados e cidades.
-   `applications/denuncias`: Destinada ao gerenciamento de denúncias (provavelmente em desenvolvimento).
-   `applications/gestao_publica`: Relacionada à gestão pública (provavelmente em desenvolvimento).

## Como Começar

### 1. Instalar Dependências

Certifique-se de que seu ambiente virtual está ativado e execute:

```bash
pip install -r requirements.txt
```

### 2. Executar Migrações

Para criar as tabelas do banco de dados, incluindo o modelo de usuário customizado:

```bash
python manage.py migrate
```

### 3. Popular Dados de Localidades

Para preencher o banco de dados com estados e cidades do Brasil:

```bash
python manage.py populate_cities
```

### 4. Criar um Superusuário

Para acessar o painel de administração do Django:

```bash
python manage.py createsuperuser
```

### 5. Iniciar o Servidor

Para rodar o servidor de desenvolvimento:

```bash
python manage.py runserver
```

O servidor estará disponível em `http://127.0.0.1:8000/`.

## Endpoints da API

-   **Autenticação**: `/api/auth/` (inclui registro e login)
-   **Denúncias**: `/api/denuncias/`
-   **Localidades**: `/api/localidades/`
-   **Gestão Pública**: `/api/gestao/`

Para mais detalhes sobre os endpoints, consulte o arquivo `README.md`.

Projeto "Voz do Povo" - Manual de Instruções e Escopo Funcional

1.0 Visão Geral e Missão do Projeto

Voz do Povo é uma plataforma de tecnologia cívica de âmbito nacional para o Brasil. A missão do projeto é criar um ecossistema completo que conecta cidadãos e gestores públicos para a resolução eficiente de problemas de infraestrutura e serviços.



A plataforma funciona como um canal de comunicação estruturado, transformando reclamações pontuais em dados organizados e acionáveis. O modelo de negócio é baseado em fornecer acesso a uma plataforma de análise e resposta para entidades governamentais, garantindo a sustentabilidade do projeto e o seu impacto social.



2.0 Atores do Sistema

O sistema possui três tipos de usuários (atores), cada um com seu próprio conjunto de ferramentas e permissões:



O Cidadão: O usuário final que utiliza o aplicativo móvel (Flutter) para registrar, apoiar e acompanhar denúncias em sua comunidade.



O Gestor Público: Um representante de uma entidade governamental (Prefeitura, Governo Estadual, etc.) que acessa um portal web exclusivo para monitorar, analisar e responder oficialmente às denúncias de sua jurisdição.



O Administrador da Plataforma: O superusuário com acesso ao painel de administração central (Django Admin) para gerenciar todos os aspectos da plataforma, incluindo dados mestres, usuários e moderação de conteúdo.



3.0 Modelo de Dados e Entidades Principais

O sistema é construído em torno de um conjunto de entidades de dados inter-relacionadas.



Usuário (User): Representa todos os atores que podem se logar no sistema (Cidadãos e Gestores Públicos). Contém informações básicas como nome, e-mail e senha (armazenada de forma segura com hash).



Localidades (Estado e Cidade): Tabelas pré-populadas com todos os estados e municípios do Brasil (baseadas em dados do IBGE). Cada cidade está associada a um estado.



Categoria (Categoria): Define os tipos de problemas que podem ser reportados (ex: "Iluminação Pública", "Saneamento", "Condições da Via"). Esta é uma lista gerenciada pelo Administrador da Plataforma.



Denúncia (Denuncia): A entidade central do sistema. Cada denúncia representa o "Card" principal de um problema e contém:



Associação: Ligada a um autor (Usuário), uma Categoria, uma Cidade e um Estado.



Conteúdo: Título, descrição textual e um campo de foto, que é obrigatório.



Geolocalização: As coordenadas geográficas exatas (latitude/longitude) do problema.



Jurisdição: A esfera de responsabilidade pelo problema (Municipal, Estadual, Federal ou Privado).



Status: O estado atual da denúncia (Aberta, Em Análise, Resolvida, etc.).



Apoio (ApoioDenuncia): Representa uma reclamação subsequente que foi agrupada a uma Denúncia principal. Cada Apoio está ligado a uma única Denúncia e a um usuário apoiador.



Entidade Oficial (OfficialEntity): Representa a instituição governamental (ex: "Prefeitura Municipal de Porto Alegre"). Está associada a uma localidade (cidade ou estado) e a um ou mais Usuários (Gestores Públicos).



Resposta Oficial (OfficialResponse): A resposta formal de uma Entidade Oficial a uma Denúncia. Cada denúncia pode ter no máximo uma resposta oficial.



4.0 Arquitetura e Stack de Tecnologia

A plataforma utiliza uma arquitetura de microsserviços desacoplada, com um frontend móvel e um backend central.



Backend:



Framework: Python, utilizando Django para a estrutura principal e o portal web, e Django REST Framework (DRF) para a construção da API.



Banco de Dados: PostgreSQL com a extensão PostGIS, para suportar de forma nativa e eficiente as consultas geoespaciais.



Tarefas em Segundo Plano: Celery com Redis, para processar tarefas que não devem bloquear a interação do usuário, como o envio agendado de notificações.



Armazenamento de Arquivos: Um serviço de armazenamento em nuvem compatível com S3 para guardar as fotos enviadas pelos usuários de forma escalável.



Ambiente: O projeto é totalmente containerizado com Docker, garantindo um ambiente de desenvolvimento e produção consistente e livre de problemas de configuração de máquina.



Frontend:



Framework: Flutter, para a criação de um aplicativo móvel multiplataforma (iOS e Android) a partir de uma única base de código.



Arquitetura: Segue os princípios de Feature-First e Clean Architecture, garantindo um código organizado, testável e escalável.



Gerenciamento de Estado: Riverpod, para um gerenciamento de estado reativo e eficiente.



Navegação: GoRouter, para um sistema de rotas robusto e centralizado.



5.0 Escopo Funcional Detalhado

5.1. O Aplicativo Cidadão (Flutter)



Autenticação Segura: O processo de cadastro exige verificação em duas etapas por e-mail, garantindo a validade dos usuários. O login utiliza um sistema de tokens de acesso e atualização para manter a sessão segura e contínua.



Fluxo de Criação de Denúncia:



O usuário inicia o fluxo e escolhe entre usar sua localização GPS atual ou selecionar um local manualmente em um mapa interativo.



Com as coordenadas definidas, o aplicativo consulta a API, que retorna a cidade, o estado e a jurisdição sugerida para aquele ponto geográfico.



O usuário é levado a um formulário onde deve obrigatoriamente anexar uma foto como prova, preencher título/descrição, selecionar uma categoria e confirmar ou corrigir a jurisdição informada pela API.



Ao submeter, a API aplica a lógica de agrupamento inteligente, decidindo se cria uma nova Denúncia ou adiciona um Apoio a uma já existente.



Visualização e Interação:



A tela principal exibe um mapa com as denúncias, com opções de filtro por localidade e categoria.



O usuário pode visualizar os detalhes de qualquer denúncia, incluindo a foto, o número de apoios, a jurisdição responsável e a Resposta Oficial, caso exista.



Ciclo de Resolução:



O autor de uma denúncia pode marcá-la como "Resolvida".



O aplicativo envia notificações push automáticas após um período de inatividade (ex: 1-2 semanas), incentivando o usuário a atualizar o status da denúncia.



5.2. O Portal de Gestão Pública (Django Web App)

Acesso Exclusivo e Pago: Um portal web seguro onde entidades governamentais assinantes podem fazer login.



Dashboard Analítico: Após o login, o gestor visualiza um painel com dados consolidados apenas de sua área de competência. O dashboard oferece:



Um mapa de calor para identificar a concentração de problemas.



Gráficos e KPIs sobre o volume e os tipos de denúncias.



Análise de tempo médio de resposta e resolução.



Canal de Resposta: O gestor pode navegar pelas denúncias, visualizar todos os detalhes (incluindo a foto) e publicar uma Resposta Oficial que se torna imediatamente visível para todos os cidadãos no aplicativo.



Gerenciamento de Status: O gestor pode atualizar o status de uma denúncia, refletindo o andamento do trabalho (ex: "Em Análise").



5.3. O Painel de Administração (Django Admin)

Interface de back-office para a gestão completa da plataforma pelo Administrador.



Permite a gestão de todos os dados mestres do sistema, como a lista de Cidades, Estados e Categorias de problemas.



Fornece ferramentas para moderação de conteúdo (revisar denúncias e fotos) e gerenciamento de todos os usuários (Cidadãos e Gestores Públicos).



6.0 Contrato da API (Fluxo de Dados Essencial)

Autenticação: A API expõe endpoints para todo o fluxo de autenticação, desde o registro em duas etapas até a renovação de tokens.



Análise de Local: Um endpoint dedicado recebe coordenadas geográficas e retorna a localidade e a jurisdição sugerida, sem a necessidade de autenticação.



Criação de Denúncia: O principal endpoint de criação recebe uma requisição contendo a foto, os dados textuais (título, descrição, etc.) e as coordenadas. Ele executa a lógica de agrupamento e retorna o objeto da denúncia (nova ou existente).



Listagem de Denúncias: Um endpoint para listar as denúncias, que suporta paginação e múltiplos filtros (localidade, categoria, status) para alimentar as telas do aplicativo e do portal de gestão.



Ações do Usuário: Endpoints específicos para ações como "Marcar como Resolvido".



Ações do Gestor Público: Endpoints seguros para que o portal de gestão possa publicar respostas e atualizar o status das denúncias.



Arquitetura, Organização de Código e Boas Práticas do Projeto "Voz do Povo"

Este documento serve como o guia arquitetural para o desenvolvimento da plataforma, estabelecendo onde cada parte do código deve residir e quais padrões devem ser seguidos e evitados.



1.0 A Arquitetura: Separação de Responsabilidades

A filosofia central é a separação de responsabilidades. A interface do usuário (UI) não deve conhecer as regras de negócio, e as regras de negócio não devem conhecer a origem dos dados (banco de dados, API externa, etc.).



1.1. Backend (Arquitetura Django por "Apps")



O backend será organizado em "Apps" modulares do Django, onde cada App representa uma funcionalidade ou um domínio de negócio claro do sistema.



App core: Contém o modelo de User customizado, configurações base e funcionalidades compartilhadas por todo o projeto.



App autenticacao: Responsável por todo o fluxo de registro, login, tokens e recuperação de senha.



App localidades: Gerencia os modelos de Estado e Cidade.



App denuncias: O coração do sistema. Gerencia os modelos Categoria, Denuncia, ApoioDenuncia e toda a lógica de agrupamento geoespacial.



App gestao_publica: Gerencia os modelos OfficialEntity, OfficialResponse e contém a lógica do portal web para os gestores públicos.



Dentro de cada App, a separação de responsabilidades é mantida:



models.py: Define a estrutura do banco de dados.



views.py: Orquestra as requisições HTTP, valida os dados de entrada (usando Serializers) e retorna as respostas. Não deve conter regras de negócio complexas.



serializers.py: Valida e transforma os dados entre o formato JSON da API e os objetos do Django.



services.py (ou logic.py): Arquivo opcional para conter a lógica de negócio complexa. Por exemplo, a lógica de "agrupamento de denúncias" viveria aqui, sendo chamada pela View.



1.2. Frontend (Arquitetura Limpa Adaptada - Flutter)



O frontend seguirá a arquitetura "Feature-First" e os princípios da Clean Architecture, conforme já estabelecido na documentação inicial do projeto.





Feature-First: O código é organizado em pastas por funcionalidade (ex: autenticacao, denuncias), facilitando a localização e manutenção.





Separação de Camadas: Dentro de cada funcionalidade, o código é dividido em duas camadas principais:



Camada de Dados (data): Responsável por obter os dados, seja de uma API ou de um banco de dados local.



models: Define as estruturas de dados (ex: classe Denuncia).





datasources: Faz a chamada HTTP real para a API usando o Dio.







repositories: Abstrai a fonte de dados, tratando erros e fornecendo uma interface limpa para a camada de apresentação.





Camada de Apresentação (presentation): Responsável por exibir a UI e gerenciar o estado da tela.





view (ou pages/screens): Contém os widgets que compõem as telas do aplicativo.



viewmodel (ou notifiers): Contém a lógica da UI e gerencia o estado da tela usando Riverpod. É o intermediário entre a View e o Repository.



widgets: Contém widgets menores e reutilizáveis específicos daquela funcionalidade.



2.0 Organização de Pastas (Onde Cada Coisa Deve Ficar)
2.1. Estrutura do Backend (Django)
2.2. Estrutura do Frontend (Flutter)



voz_do_povo_flutter/


3.0 O Que Não Fazer (Anti-padrões e Convenções)

Seguir estas regras é crucial para manter a qualidade do código.



3.1. Regras Gerais (Backend e Frontend)



❌ Anti-padrão: Colocar lógica de negócio (cálculos, regras de validação complexas, orquestração de múltiplas ações) diretamente nas Views (Django) ou nos Widgets de UI (Flutter).



✅ Boa Prática: A lógica de negócio deve residir em services.py (Backend) ou nos ViewModels/Notifiers e Repositories (Frontend). As Views/Widgets devem ser o mais "burras" possível, responsáveis apenas por exibir dados e capturar eventos do usuário.



❌ Anti-padrão: Deixar chaves de API, senhas ou URLs de ambiente fixas no código (hardcoded).



✅ Boa Prática: Utilizar arquivos de ambiente (.env) para todas as configurações sensíveis ou que mudam entre os ambientes de desenvolvimento e produção.



❌ Anti-padrão: Repetir o mesmo trecho de código em vários lugares (ex: a mesma função de formatação de data).



✅ Boa Prática: Abstrair funcionalidades reutilizáveis em classes de utilitários ou helpers, localizados em uma pasta utils ou helpers dentro do core ou do app correspondente.



3.2. Específico do Backend (Django)



❌ Anti-padrão: Fazer consultas ao banco de dados dentro de um laço (for loop), causando o problema de "N+1 queries" e lentidão.



✅ Boa Prática: Utilizar as funções select_related e prefetch_related do Django para carregar os dados relacionados em uma única consulta antes do laço.



❌ Anti-padrão: Colocar todos os endpoints da aplicação no arquivo urls.py principal do projeto.



✅ Boa Prática: Cada App Django deve ter seu próprio arquivo urls.py, que é incluído no arquivo principal. Isso mantém a modularidade.



3.3. Específico do Frontend (Flutter)



❌ Anti-padrão: Fazer chamadas de API (usando Dio) diretamente de um Widget (dentro de um StatelessWidget ou StatefulWidget).



✅ Boa Prática: Todas as chamadas de API devem ser feitas exclusivamente pela camada de DataSource. A UI só deve interagir com o Repository ou o ViewModel.



❌ Anti-padrão: Criar widgets monolíticos e gigantes com centenas de linhas de código.



✅ Boa Prática: Quebrar a UI em componentes menores, reutilizáveis e focados em uma única responsabilidade. Colocar widgets específicos de uma feature na pasta widgets daquela feature, e widgets genéricos (botões, campos de texto customizados) na pasta core/widgets.



❌ Anti-padrão: Gerenciar estado complexo (loading, error, success, dados do formulário) usando setState() em um StatefulWidget.



✅ Boa Prática: Utilizar os Notifiers do Riverpod (NotifierProvider, AsyncNotifierProvider) para gerenciar todo o estado que não seja puramente local e efêmero de um widget.