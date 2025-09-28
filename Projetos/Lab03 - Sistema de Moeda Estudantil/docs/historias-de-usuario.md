# 📖 Histórias de Usuário — Sistema de Moeda Estudantil

As histórias de usuário descrevem **funcionalidades vistas pela perspectiva dos usuários finais**, alinhadas ao escopo definido nos diagramas e requisitos.

## 👨‍🎓 Aluno
### US01 — Cadastrar-se no sistema
- **Como aluno**, quero me cadastrar informando meus dados pessoais e acadêmicos  
- **Para que** eu possa acessar o sistema e receber moedas.
**Aceite:** nome, e-mail, CPF, RG, endereço, instituição e curso; evitar duplicidade de e-mail/CPF.

### US02 — Autenticar-se (login)
- **Como aluno**, quero autenticar-me com e-mail e senha  
- **Para que** eu possa acessar minha carteira e funcionalidades.
**Aceite:** validar credenciais; bloquear acesso sem login.

### US03 — Consultar saldo e extrato
- **Como aluno**, quero consultar meu saldo de moedas e extrato  
- **Para que** eu saiba quantas moedas tenho e de onde vieram.
**Aceite:** exibir saldo atual e histórico com data, valor e origem.

### US04 — Receber moedas
- **Como aluno**, quero receber moedas de professores  
- **Para que** meu desempenho e participação sejam reconhecidos.
**Aceite:** creditar automaticamente e enviar e-mail.

### US05 — Trocar moedas por vantagens
- **Como aluno**, quero trocar minhas moedas por vantagens cadastradas  
- **Para que** eu possa resgatar recompensas.
**Aceite:** verificar saldo, debitar custo, gerar cupom/código, e-mails para aluno e empresa.

## 👨‍🏫 Professor
### US06 — Autenticar-se (login)
### US07 — Consultar extrato
### US08 — Enviar moedas a um aluno (com motivo)
**Aceite:** validar saldo; motivo obrigatório; registrar transação.
Obs.: Professor recebe 1.000 moedas/semestre (saldo acumulável).

## 🏢 Empresa Parceira
### US09 — Cadastrar-se como empresa parceira
### US10 — Cadastrar vantagem (título, descrição, imagem, custo)
### US11 — Visualizar resgates

## 🏛️ Instituição
### US12 — Cadastrar/validar empresas parceiras
