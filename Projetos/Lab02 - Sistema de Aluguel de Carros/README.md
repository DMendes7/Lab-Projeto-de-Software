# 🚗 AutoRent - Sistema de Aluguel de Carros

![Hero Banner](car-rental-system/src/main/resources/static/img/hero-banner.png)

AutoRent é um sistema acadêmico desenvolvido como **projeto de laboratório** para a disciplina de Engenharia de Software.  
O objetivo é simular um sistema moderno de gerenciamento de uma locadora de automóveis, com foco em **boas práticas de desenvolvimento**, **UI/UX moderna** e **funcionalidades completas**.

---

## ✨ Funcionalidades

- Cadastro e gerenciamento de **Automóveis**
- Cadastro e gerenciamento de **Contratantes**
- Criação e acompanhamento de **Pedidos**
- Aprovação/Reprovação de pedidos diretamente nos **detalhes**
- Banco de dados em **H2** com possibilidade de **seeding inicial**
- Interface **dark mode** responsiva e moderna
- Notificações de sucesso/erro com **animações**
- Componentes customizados (**switch de ativo**, botões estilizados, badges de status, etc.)

---

## 🖼️ Screenshots

### Tela Inicial
![Tela Inicial](car-rental-system/src/main/resources/static/img/home.png)

### Lista de Automóveis
![Lista de Automóveis](car-rental-system/src/main/resources/static/img/ista-automoveis.png)

### Cadastro de Automóvel
![Cadastro Automóvel](car-rental-system/src/main/resources/static/img/cadastro-automovel.png)

### Lista de Contratantes
![Lista Contratantes](car-rental-system/src/main/resources/static/img/lista-contratantes.png)

### Cadastro de Contratante
![Cadastro Contratante](car-rental-system/src/main/resources/static/img/cadastro-contratante.png)

### Lista de Pedidos
![Lista Pedidos](car-rental-system/src/main/resources/static/img/lista-pedidos.png)

### Detalhes de Pedido + Aprovação
![Detalhes Pedido](car-rental-system/src/main/resources/static/img/detalhes-pedido.png)

---

## 🛠️ Tecnologias

- **Java 17** + **Spring Boot 3**
- **Thymeleaf** para templates dinâmicos
- **Spring Data JPA** + **H2 Database**
- **Maven** como gerenciador de dependências
- **HTML5 + CSS3 (customizado)**  
- **JavaScript** para interatividade
- **Notificações animadas** e **UI responsiva**

---

## ⚙️ Como rodar o projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/DMendes7/Lab-Projeto-de-Software.git
   cd Projetos/Lab02 - Sistema de Aluguel de Carros
   cd car-rental-system
   ```

2. Compile e rode com Maven:
   ```bash
   mvn spring-boot:run
   ```

3. Acesse no navegador:
   ```
   http://localhost:8080
   ```

---

## 📂 Estrutura do Projeto

```
car-rental-system/
├── src/
│   ├── main/
│   │   ├── java/com/carrental/...    # Código fonte
│   │   ├── resources/
│   │   │   ├── static/css            # Estilos (style.css)
│   │   │   ├── static/js             # Scripts (notifications.js)
│   │   │   └── templates             # Páginas HTML (Thymeleaf)
│   └── test/                         # Testes automatizados
├── img/                              # Imagens para o README
└── README.md
```

---

## 👨‍💻 Autor

Projeto acadêmico desenvolvido por **Davi Mendes**  
PUC Minas - Engenharia de Software

[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/dmendes7)
[![GitHub](https://img.shields.io/badge/GitHub-black?style=flat&logo=github)](https://github.com/DMendes7)

---

## 📜 Licença

Este projeto é apenas para fins acadêmicos.  
Uso livre para aprendizado, mas não para produção comercial.
