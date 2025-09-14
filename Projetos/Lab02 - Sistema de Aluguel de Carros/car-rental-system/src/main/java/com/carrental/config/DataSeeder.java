package com.carrental.config;

import com.carrental.model.Automovel;
import com.carrental.model.Contratante;
import com.carrental.model.Pedido;
import com.carrental.model.StatusPedido;
import com.carrental.repository.AutomovelRepository;
import com.carrental.repository.ContratanteRepository;
import com.carrental.repository.PedidoRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.time.LocalDate;

@Configuration
public class DataSeeder {

    @Bean
    CommandLineRunner seedData(
            ContratanteRepository contratanteRepo,
            AutomovelRepository automovelRepo,
            PedidoRepository pedidoRepo
    ) {
        return args -> {
            // só popula se estiver vazio (não duplica em reinícios)
            if (contratanteRepo.count() > 0 || automovelRepo.count() > 0 || pedidoRepo.count() > 0) return;

            Contratante c1 = new Contratante();
            c1.setNome("João Silva"); c1.setCpf("123.456.789-00"); c1.setRg("MG-12.345.678");
            c1.setEndereco("Rua A, 100"); c1.setProfissao("Engenheiro");
            contratanteRepo.save(c1);

            Contratante c2 = new Contratante();
            c2.setNome("Maria Souza"); c2.setCpf("987.654.321-00"); c2.setRg("MG-87.654.321");
            c2.setEndereco("Av. B, 200"); c2.setProfissao("Analista");
            contratanteRepo.save(c2);

            Automovel a1 = new Automovel();
            a1.setRenavam("0099887766"); a1.setAno(2021); a1.setMarca("Toyota"); a1.setModelo("Corolla");
            a1.setPlaca("ABC1D23"); a1.setAtivo(true);
            automovelRepo.save(a1);

            Automovel a2 = new Automovel();
            a2.setRenavam("1122334455"); a2.setAno(2022); a2.setMarca("Fiat"); a2.setModelo("Pulse");
            a2.setPlaca("EFG4H56"); a2.setAtivo(true);
            automovelRepo.save(a2);

            Pedido p1 = new Pedido();
            p1.setContratante(c1);
            p1.setAutomovel(a1);
            p1.setPeriodoInicio(LocalDate.now().plusDays(1));
            p1.setPeriodoFim(LocalDate.now().plusDays(7));
            p1.setStatus(StatusPedido.NOVO);
            pedidoRepo.save(p1);

            Pedido p2 = new Pedido();
            p2.setContratante(c2);
            p2.setAutomovel(a2);
            p2.setPeriodoInicio(LocalDate.now().plusDays(3));
            p2.setPeriodoFim(LocalDate.now().plusDays(10));
            p2.setStatus(StatusPedido.EM_AVALIACAO);
            pedidoRepo.save(p2);
        };
    }
}
