# 📖 Histórias de Usuário - Sistema de Moeda Estudantil
> Documento de backlog funcional visto pela perspectiva dos usuários finais (Aluno, Professor, Empresa Parceira e Instituição).  
> Cada história traz um objetivo claro e **critérios de aceite** verificáveis.
---
## 📚 Sumário
- [Contexto](#contexto)
- [Definições rápidas](#definições-rápidas)
- [👨‍🎓 Aluno](#-aluno)
 - US01 - Cadastrar-se
 - US02 - Autenticar-se (login)
 - US03 - Consultar saldo e extrato
 - US04 - Receber moedas
 - US05 - Trocar moedas por vantagens
 - **US13 - Histórico de transações do aluno**
- [👨‍🏫 Professor](#-professor)
 - US06 - Autenticar-se (login)
 - US07 - Consultar extrato
 - US08 - Enviar moedas a um aluno (com motivo)
- [🏢 Empresa Parceira](#-empresa-parceira)
 - US09 - Cadastrar-se como empresa parceira
 - US10 - Cadastrar vantagem (título, descrição, imagem, custo)
 - US11 - Visualizar resgates
- [🏛️ Instituição](#-instituição)
 - US12 - Cadastrar/validar empresas parceiras
---
## Contexto
A plataforma de **Moeda Estudantil** permite que professores distribuam moedas a alunos por participação/desempenho; alunos usam essas moedas para **resgatar vantagens** de **empresas parceiras**. A instituição faz a curadoria dos parceiros.
## Definições rápidas
- **Moeda**: crédito digital interno.
- **Carteira**: saldo e movimentações do usuário.
- **Vantagem**: benefício ofertado por empresa parceira (tem **custo em moedas**).
- **Cupom**: comprovante/código gerado no resgate.
---
## 👨‍🎓 Aluno
### US01 - Cadastrar-se no sistema
**Como** aluno, **quero** me cadastrar informando meus dados pessoais e acadêmicos  
**para** poder acessar o sistema e receber moedas.
**Aceite**
- Campos mínimos: **nome**, **e-mail**, **senha**, **CPF**, **RG**, **endereço**, **instituição** e **curso**.
- **E-mail/CPF** não podem se repetir (unicidade).
- Confirmação de cadastro via feedback (mensagem/redirect).
---
### US02 - Autenticar-se (login)
**Como** aluno, **quero** autenticar-me com e-mail e senha  
**para** acessar minha carteira e funcionalidades.
**Aceite**
- Validação de credenciais; mensagens claras em caso de erro.
- Impedir o acesso às rotas privadas sem login.
- Opção de **logout**.
---
### US03 - Consultar saldo e extrato
**Como** aluno, **quero** consultar meu **saldo** de moedas e um **extrato básico**  
**para** saber quantas moedas tenho e de onde vieram.
**Aceite**
- Exibir **saldo atual**.
- Exibir histórico **ordenado por data desc** com: **data/hora**, **tipo** (crédito/débito), **valor**, **descrição**/**origem**.
---
### US04 - Receber moedas
**Como** aluno, **quero** receber moedas enviadas por professores  
**para** que meu desempenho/participação seja reconhecido.
**Aceite**
- Crédito automático na **carteira**.
- Registro no **histórico**.
- **E-mail** de notificação.
---
### US05 - Trocar moedas por vantagens
**Como** aluno, **quero** trocar minhas moedas por vantagens cadastradas  
**para** resgatar recompensas.
**Aceite**
- Verificação de **saldo suficiente**.
- Débito do valor da vantagem.
- **Criação de cupom** (código único), com vínculo ao resgate.
- Registro no **histórico**.
- Envio de e-mail ao aluno com **cupom** e à empresa com **notificação de resgate**.
- Impedir resgates duplicados de uma mesma vantagem quando definido pela oferta.
---
### US13 - Histórico de transações do aluno
**Como** aluno, **quero** visualizar um **histórico detalhado de transações**  
**para** entender cada crédito/débito e acompanhar a evolução do meu saldo.
**Aceite**
- Listar **todas as movimentações**:  
 - **Créditos**: envios de professores, estornos, bônus.  
 - **Débitos**: resgates de vantagens, ajustes administrativos.
- Cada linha deve mostrar: **data/hora**, **tipo** (crédito/débito), **valor**, **descrição/motivo**, **referência** (ex.: professor/empresa, vantagem/código do cupom), e **saldo após a transação**.
- **Ordenação** padrão por data desc.
- Links/contexto quando existir: clicar em uma transação de débito deve apontar para a **vantagem/cupom** relacionado.
---
## 👨‍🏫 Professor
### US06 - Autenticar-se (login)
**Como** professor, **quero** realizar login  
**para** acessar as ações de envio de moedas e acompanhar registros.
**Aceite**
- Mesmos critérios de autenticação do aluno; perfis/roles distintos.
---
### US07 - Consultar extrato
**Como** professor, **quero** consultar um extrato  
**para** visualizar meus envios e eventuais recebimentos.
**Aceite**
- Exibir **envios de moedas** realizados (com aluno, motivo e valor).
- Filtros por **período** e **aluno** (opcional).
- Paginação.
---
### US08 - Enviar moedas a um aluno (com motivo)
**Como** professor, **quero** enviar moedas para um aluno, informando um **motivo**  
**para** reconhecer participação/desempenho.
**Aceite**
- Campo **motivo** obrigatório.
- Verificar **saldo do professor** (regra: 1.000 moedas/semestre; saldo **acumulável**).
- Registro no **histórico** do professor (**débito**) e do aluno (**crédito**).
- Confirmação visual de envio e mensagens de erro claras.
---
## 🏢 Empresa Parceira
### US09 - Cadastrar-se como empresa parceira
**Como** empresa, **quero** me cadastrar  
**para** disponibilizar vantagens aos alunos.
**Aceite**
- Campos mínimos: **razão social**, **CNPJ**, **e-mail**, **telefone**, **endereço**.
- Fluxo de **validação/ativação** pela instituição (status: pendente/ativo/inativo).
---
### US10 - Cadastrar vantagem (título, descrição, imagem, custo)
**Como** empresa, **quero** cadastrar vantagens  
**para** atrair alunos com benefícios.
**Aceite**
- Campos: **título**, **descrição**, **imagem** (upload), **custo em moedas**, **regras/observações**.
- Mostrar **prévia** (thumb) no catálogo.
- Vantagem pode ter **limite por aluno** (opcional) e **quantidade total** (opcional).
---
### US11 - Visualizar resgates
**Como** empresa, **quero** visualizar os **cupons resgatados**  
**para** controlar atendimentos e validações.
**Aceite**
- Listar **cupons** com **aluno**, **data**, **código**, **status** (ativo/usado/expirado).
- Busca por **código** e filtros por **período/status**.
- Ação de **marcar cupom como utilizado** (se aplicável).
---
## 🏛️ Instituição
### US12 - Cadastrar/validar empresas parceiras
**Como** instituição, **quero** aprovar/gerenciar empresas parceiras  
**para** garantir segurança e qualidade das ofertas.
**Aceite**
- Painel para **aprovar/reprovar/desativar** empresas.
- Visão geral de **ofertas** e **resgates** por parceiro.
- Logs de auditoria (mínimos).
---
## Regras de negócio e políticas
- **Saldo do Professor**: 1.000 moedas/semestre, **acumuláveis** entre semestres.
- **Envio de moedas** exige **motivo** textual.
- **Resgate** debita o custo, gera **cupom** único e cria **transação** vinculada.
- **Duplicidade de resgate**: impedir conforme regra da vantagem (por aluno/por período).
- **Notificações por e-mail**:  
 - Resgate: enviar para **aluno** (com código) e **empresa** (notificação).
 - Opcional: recebimento de moedas pelo aluno.
---
## Requisitos não funcionais (RNF)
- **Segurança**: autenticação por sessão; perfis por **role** (ALUNO, PROFESSOR, EMPRESA, INSTITUICAO); autorização por rota.
- **Disponibilidade**: 99% para ambiente de produção acadêmico.
- **Performance**: listagens paginadas; consultas usando `select_related/prefetch_related` onde couber.
- **Armazenamento de mídia**: imagens de vantagens com tamanho/formatos controlados.
- **E-mails**: templates HTML/TXT e fallback de envio.
- **Observabilidade**: logs de erro e eventos importantes (envios, resgates, estornos).
- **Acessibilidade**: contraste adequado; navegação por teclado; rótulos em formulários.
- **Internacionalização**: strings em PT-BR centralizadas para fácil ajuste futuro.
---
