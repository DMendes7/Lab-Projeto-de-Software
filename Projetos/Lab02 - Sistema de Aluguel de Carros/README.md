# 🚗 AutoRent — Sistema de Aluguel de Carros

![Hero Banner](car-rental-system/src/main/resources/static/img/hero.jpg)

**AutoRent** é um sistema acadêmico para gerenciamento de locadora de veículos, com foco em **boas práticas**, **UI/UX moderna**, **controle de acesso por perfil** e fluxo completo de **Automóveis**, **Contratantes** e **Pedidos**.

---

## 🔗 Deploy (Render)

> Coloque aqui o link público do seu deploy:

**👉 Acesse:** https://autorent-vjm1.onrender.com/

---

## ✨ Funcionalidades

- **Autenticação & Autorização (Spring Security)**
  - Login via `/login`
  - Perfis: **ADMIN** (acesso total) e **CLIENT** (apenas seus pedidos)
  - Header global com estado de login e **logout**
- **Automóveis**: cadastro, listagem, edição, remoção
- **Contratantes**: cadastro, listagem, edição, remoção
- **Pedidos**:
  - criação, edição, exclusão
  - **detalhe do pedido** com ações de aprovar/reprovar/iniciar execução
  - status: `NOVO`, `EM_AVALIACAO`, `APROVADO`, `REPROVADO`, `EM_EXECUCAO`, `CANCELADO`
- **UI moderna (dark)**, responsiva, com **toasts** de sucesso/erro
- **Fragments Thymeleaf**: header compartilhado em todas as páginas
- **H2** em memória (DEV) com **semeadura opcional** (via `DataSeeder` *ou* `data.sql`)

---

## 👥 Usuários de Teste (pré-carregados)

| Perfil | E-mail               | Senha |
|------: |----------------------|-------|
| ADMIN  | `admingia@demo.com`  | `*****`|
| CLIENT | `alice@demo.com`     | `****` |
| CLIENT | `bruno@demo.com`     | `****` |

> Observação: existem **Contratantes** correspondentes a Alice e Bruno, para você vincular pedidos a eles.  
> Se usar `data.sql` no deploy, esses registros podem ser criados automaticamente.

---

## 🖼️ Telas (exemplos)

- Início
- Listas e formulários (Automóveis, Contratantes, Pedidos)
- Detalhe do Pedido com ações (aprovar/reprovar/iniciar)

As imagens de exemplo ficam em `car-rental-system/src/main/resources/static/img/`.

---

## 🗂️ Estrutura do Repositório

> O projeto fica **dentro** da pasta `Projetos/Lab02 - Sistema de Aluguel de Carros/car-rental-system`.

```
Projetos/
└── Lab02 - Sistema de Aluguel de Carros/
    └── car-rental-system/
        ├── Dockerfile
        ├── pom.xml
        ├── src/
        │   └── main/
        │       ├── java/com/carrental/
        │       │   ├── config/
        │       │   │   ├── WebConfig.java
        │       │   │   └── WebSecurityConfig.java
        │       │   ├── controller/
        │       │   │   ├── AutomovelController.java
        │       │   │   ├── ContratanteController.java
        │       │   │   └── PedidoController.java
        │       │   ├── model/ (Automovel, Contratante, Pedido, enums)
        │       │   ├── repository/ (interfaces JPA)
        │       │   └── service/ (AutomovelService, ContratanteService, PedidoService)
        │       └── resources/
        │           ├── application.properties
        │           ├── static/
        │           │   ├── css/style.css
        │           │   ├── js/notifications.js
        │           │   └── img/...
        │           └── templates/
        │               ├── fragments/header.html
        │               ├── index.html
        │               ├── login.html
        │               ├── automovel-list.html
        │               ├── automovel-form.html
        │               ├── contratante-list.html
        │               ├── contratante-form.html
        │               ├── pedido-list.html
        │               ├── pedido-form.html
        │               └── pedido-detalhe.html
        └── README.md
```

**Fragmento de Header (Thymeleaf)**  
Inclusão nos templates:
```html
<th:block th:replace="~{fragments/header :: header}"></th:block>
```

---

## ⚙️ Como Rodar Localmente

### 1) Clonar e entrar no projeto

```bash
git clone https://github.com/DMendes7/Lab-Projeto-de-Software.git
cd "Projetos/Lab02 - Sistema de Aluguel de Carros/car-rental-system"
```

### 2) Rodar com Maven

```bash
mvn spring-boot:run
```

Acesse: `http://localhost:8080`

---

## 🐳 Rodando com Docker (local)

Requer **Docker** instalado.

```bash
# na raiz de car-rental-system (onde está o Dockerfile)
docker build -t autorent .
docker run -p 8080:8080 --name autorent autorent
# acessar: http://localhost:8080
```

---

## 🔐 Rotas & Acesso

- **/login**: página de login
- **/**: home
- **/contratantes/**
  - ADMIN: total
  - CLIENT: oculto/no acesso
- **/automoveis/**
  - ADMIN: total
  - CLIENT: oculto/no acesso
- **/pedidos/**
  - ADMIN: vê e gerencia todos
  - CLIENT: vê **apenas os seus**
- **/logout**: encerra sessão

---

## 🛠️ Tecnologias

- **Java 17**, **Spring Boot 3**
- **Thymeleaf**, **Spring Data JPA**
- **Spring Security**
- **H2** (DEV)
- **Maven**
- **Docker**
- **HTML/CSS/JS** (UI moderna, dark, responsiva)

---

## 👨‍💻 Autor

Projeto acadêmico desenvolvido por **Davi Mendes** — PUC Minas (Engenharia de Software)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/dmendes7)
[![GitHub](https://img.shields.io/badge/GitHub-black?style=flat&logo=github)](https://github.com/DMendes7)

---

## 📜 Licença

Projeto para fins acadêmicos.  
Uso livre para estudo/demonstração (não recomendado para produção).
