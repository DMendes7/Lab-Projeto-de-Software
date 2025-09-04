# 📖 Histórias de Usuário - Sistema de Aluguel de Carros
**Sprint 1 (Lab02S01)**  
Disciplina: Laboratório de Desenvolvimento de Software  
Professor: João Paulo C. Aramuni  

---

## 👤 Cliente

### História: Criar Pedido de Aluguel
**Como** cliente  
**Quero** registrar um pedido de aluguel informando veículo, período e forma de pagamento  
**Para** que eu possa solicitar um carro e acompanhar seu status.  

**Critérios de Aceite**
- Pedido só é criado se o cliente estiver autenticado/cadastrado.  
- Veículo selecionado deve estar cadastrado no sistema.  
- Após criar, o status inicial é **“Em avaliação”**.  
- O cliente pode consultar o status do pedido.  

---

### História: Consultar Pedido
**Como** cliente  
**Quero** visualizar meus pedidos em andamento  
**Para** acompanhar a situação atual (Novo, Em avaliação, Aprovado, Reprovado, Em execução, Cancelado).  

**Critérios de Aceite**
- Posso listar todos os pedidos vinculados ao meu usuário.  
- Cada pedido exibe status, dados básicos e veículo associado.  

---

### História: Alterar Pedido
**Como** cliente  
**Quero** alterar os dados do meu pedido antes da aprovação  
**Para** corrigir informações sem precisar cancelar.  

**Critérios de Aceite**
- Só é possível alterar enquanto o pedido estiver em status **“Novo” ou “Em avaliação”**.  
- Alterações ficam registradas em histórico.  

---

### História: Cancelar Pedido
**Como** cliente  
**Quero** cancelar um pedido antes da aprovação  
**Para** não gerar cobrança nem vínculo desnecessário.  

**Critérios de Aceite**
- Cancelamento só permitido enquanto status = **Novo** ou **Em avaliação**.  
- Após cancelamento, status final = **Cancelado** e não pode ser revertido.  

---

## 👔 Agente / Banco

### História: Avaliar Pedido
**Como** agente/banco  
**Quero** analisar os pedidos submetidos pelos clientes com dados de contratante e rendimentos  
**Para** decidir se aprovo ou reprovo o aluguel.  

**Critérios de Aceite**
- Posso visualizar os dados completos do contratante (até 3 rendimentos).  
- Posso aprovar/reprovar com justificativa.  
- Status muda automaticamente para **Aprovado** ou **Reprovado**.  

---

### História: Modificar Pedido (Agente/Banco)
**Como** agente/banco  
**Quero** ajustar dados de pedidos submetidos  
**Para** adequar informações antes da decisão final.  

**Critérios de Aceite**
- Posso editar campos restritos (ex.: datas, observações).  
- Alteração fica registrada em histórico.  

---

### História: Aprovar Execução de Contrato
**Como** agente/banco  
**Quero** confirmar a execução de um pedido aprovado  
**Para** que seja gerado o contrato de aluguel.  

**Critérios de Aceite**
- Só é permitido após parecer positivo na avaliação financeira.  
- Contrato fica vinculado ao pedido.  

---

### História: Associar Contrato de Crédito
**Como** banco  
**Quero** associar um contrato de crédito ao pedido de um cliente  
**Para** viabilizar o aluguel quando há financiamento.  

**Critérios de Aceite**
- Contrato contém banco, número, taxa e data de aprovação.  
- Só pode ser associado se o banco for o agente responsável pela análise.  

---

## 🛠️ Atendente/Admin

### História: Gerir Dados do Contratante
**Como** atendente/admin  
**Quero** cadastrar e atualizar informações de clientes (RG, CPF, endereço, profissão, empregadores e rendimentos)  
**Para** manter dados consistentes para avaliação e contratos.  

**Critérios de Aceite**
- Cada contratante pode ter até 3 rendimentos cadastrados.  
- Dados obrigatórios: RG, CPF, Nome, Endereço.  

---

### História: Gerir Automóvel
**Como** atendente/admin  
**Quero** cadastrar e atualizar veículos (RENAVAM, ano, marca, modelo, placa)  
**Para** disponibilizar automóveis válidos para locação.  

**Critérios de Aceite**
- Placa e RENAVAM devem ser únicos.  
- Só veículos ativos podem ser vinculados a pedidos.  


---

