# scripts/seed_demo.py
from django.contrib.auth import get_user_model
from apps.institutions.models import Instituicao
from apps.accounts.models import Aluno, Professor
from apps.wallet.services import CarteiraService
from apps.wallet.models import Carteira
from apps.partners.models import EmpresaParceira
from apps.catalog.models import Vantagem
from apps.transactions.services import TransacaoService
from apps.catalog.services import CatalogoService

User = get_user_model()

def main():
    # 1) Instituição
    inst, _ = Instituicao.objects.get_or_create(nome="PUC Demo")

    # 2) Usuários (senha 123)
    def mkuser(username, role, email=None):
        u, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email or f"{username}@demo.local", "role": role},
        )
        if created:
            u.set_password("123")
            u.save()
        return u

    prof1 = mkuser("prof1", "PROFESSOR", "prof1@demo.local")
    prof2 = mkuser("prof2", "PROFESSOR", "prof2@demo.local")
    alu1  = mkuser("aluno1", "ALUNO", "aluno1@demo.local")
    alu2  = mkuser("aluno2", "ALUNO", "aluno2@demo.local")

    # 3) Perfis
    Professor.objects.get_or_create(user=prof1, defaults={"cpf":"111.111.111-11","departamento":"ESW","instituicao":inst,"saldo_semestral":1000})
    Professor.objects.get_or_create(user=prof2, defaults={"cpf":"222.222.222-22","departamento":"ESW","instituicao":inst,"saldo_semestral":1000})
    Aluno.objects.get_or_create(user=alu1, defaults={"cpf":"333.333.333-33","rg":"RG333","endereco":"Rua A, 10","curso":"Engenharia de Software","instituicao":inst})
    Aluno.objects.get_or_create(user=alu2, defaults={"cpf":"444.444.444-44","rg":"RG444","endereco":"Rua B, 20","curso":"Engenharia de Software","instituicao":inst})

    # 4) Carteiras
    for u in (prof1, prof2, alu1, alu2):
        CarteiraService.get_or_create(u)

    # 5) Carga inicial p/ professores (até 1000)
    for p in (prof1, prof2):
        c = Carteira.objects.get(usuario=p)
        if c.saldo < 1000:
            CarteiraService.creditar(p, 1000 - c.saldo, motivo="Carga inicial semestral")

    # 6) Empresa parceira (idempotente)
    emp, _ = EmpresaParceira.objects.update_or_create(
        cnpj="00.000.000/0001-00",
        defaults={"nome":"Loja Parceira Demo", "email":"contato@loja.demo", "ativa":True},
    )

    # 7) Vantagens
    vant1, _ = Vantagem.objects.get_or_create(
        empresa=emp, titulo="Desconto 10%",
        defaults={"descricao":"Cupom 10% em compras", "custo_moedas":50, "ativa":True},
    )
    vant2, _ = Vantagem.objects.get_or_create(
        empresa=emp, titulo="Brinde Mochila",
        defaults={"descricao":"Brinde exclusivo", "custo_moedas":80, "ativa":True},
    )

    # 8) Envios
    TransacaoService.registrar_envio(professor=prof1, aluno=alu1, valor=200, motivo="Projeto final excelente")
    TransacaoService.registrar_envio(professor=prof1, aluno=alu2, valor=150, motivo="Participação em aula")
    TransacaoService.registrar_envio(professor=prof2, aluno=alu2, valor=100, motivo="Monitoria")
    TransacaoService.registrar_envio(professor=prof2, aluno=alu1, valor= 50, motivo="Hackathon")

    # 9) Resgates
    cupom1 = CatalogoService.resgatar_vantagem(aluno=alu1, vantagem=vant1)
    cupom2 = CatalogoService.resgatar_vantagem(aluno=alu2, vantagem=vant2)

    print("✅ Seed ok.")
    print("   Professores: prof1/prof2 | Alunos: aluno1/aluno2 | senha: 123")
    print("   Cupons gerados:", cupom1.codigo, cupom2.codigo)

if __name__ == "__main__":
    main()
