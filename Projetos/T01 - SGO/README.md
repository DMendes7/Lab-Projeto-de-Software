# 🏆 SGO - Sistema de Gestão das Olimpíadas

<p align="center">
  <img src="https://img.shields.io/badge/Projeto%20de%20Software-1%C2%AA%20Entrega-blueviolet"/>
  <img src="https://img.shields.io/badge/UML%20Modelagem-Completa-blue"/>
  <img src="https://img.shields.io/badge/Professor-Jo%C3%A3o%20Paulo%20Carneiro%20Aramuni-informational"/>
</p>

## 1. 📚 Informações Gerais

Este trabalho é a primeira entrega da disciplina **Projeto de Software** [cite: 3] e contém a modelagem UML completa para o **Sistema de Gestão das Olimpíadas (SGO)**[cite: 5]. O sistema deve gerenciar competições, inscrições de atletas, alocação de locais e controle de resultados[cite: 7].

## 2. 📝 Regras de Negócio Chave

A modelagem reflete as regras de negócio [cite: 8] definidas para o sistema:

* **Cadastro:** Competições incluem modalidade, data, horário, local e lista de atletas inscritos[cite: 10].
* **Inscrição:** O atleta representa apenas um país em cada modalidade[cite: 13].
* **Alocação:** Um local só pode abrigar uma competição por vez, evitando conflitos de horário[cite: 15, 16].
* **Resultados:** Resultados são registrados para determinar os classificados em segundo e terceiro lugares[cite: 18].
* **Relatórios:** O sistema deve gerar relatórios de medalhas com base nas medalhas de ouro, prata e bronze[cite: 20].

## 3. 🏃 Histórias de Usuário (User Stories)

As Histórias de Usuário (US) [cite: 39] cobrem as funcionalidades principais do sistema:

| ID | Caso de Uso | História de Usuário (Como **[Ator]**, Eu quero **[Meta]**, Para que **[Valor]**) |
| :--- | :--- | :--- |
| **US01** | **Cadastrar Competição** | Como **Organizador**, eu quero cadastrar uma nova competição, para que o evento seja agendado. |
| **US02** | **Inscrever Atleta** | Como **Atleta**, eu quero me inscrever em uma competição, representando meu país na modalidade. |
| **US03** | **Alocar Local** | Como **Organizador**, eu quero alocar um local para uma competição, validando a ausência de conflitos de horário. |
| **US04** | **Registrar Resultados** | Como **Oficial**, eu quero registrar os resultados da competição, para que o pódio (1º, 2º, 3º) seja definido. |
| **US05** | **Relatório de Medalhas** | Como **Comitê**, eu quero gerar um relatório de medalhas por país, para que o desempenho das nações seja visualizado. |

## 4. 📐 Diagramas UML

Todos os diagramas foram desenvolvidos em PlantUML e estão dispostos abaixo[cite: 39].

### 4.1. Diagrama de Caso de Uso (UC) 🧭

<p align="center">
    <img width="500" src="img/UC-SGO.png"/>
</p>

### 4.2. Diagrama de Classes e Pacotes 🏛️

<p align="center">
    <img width="500" src="img/Class-SGO.png"/>
</p>

### 4.3. Diagrama de Componentes ⚙️

<p align="center">
    <img width="500" src="img/Component-SGO.png"/>
</p>

### 4.4. Diagrama de Pacotes 📦

<p align="center">
    <img width="500" src="img/Package-SGO.png"/>
</p>

### 4.5. Diagrama de Implantação ☁️

<p align="center">
    <img width="500" src="img/Deployment-SGO.png"/>
</p>

## 5. 🗂️ Conteúdo do Repositório (Entrega)

O repositório contém a estrutura completa exigida[cite: 43]:

* **`README.md`**: Documentação e Histórias de Usuário[cite: 47].
* **`img/`**: Contém os 5 diagramas UML em formato PNG[cite: 48, 49, 50, 51, 52].
* **`diagramas/PlantUML`**: Arquivos-fonte (`.puml`) da modelagem.
* **`diagramas/drawio`**: Arquivos de projeto editáveis (`.drawio`)[cite: 53, 54, 55, 56, 57].

---
**Próximo Passo:** **Suba este arquivo `README.md` e todos os arquivos para o GitHub.** O seu trabalho está pronto para a entrega no CANVAS[cite: 32].