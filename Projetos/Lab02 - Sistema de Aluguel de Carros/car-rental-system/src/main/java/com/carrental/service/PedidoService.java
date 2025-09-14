package com.carrental.service;

import com.carrental.model.Pedido;
import com.carrental.model.StatusPedido;
import com.carrental.repository.PedidoRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
public class PedidoService {

    private final PedidoRepository pedidoRepository;

    public PedidoService(PedidoRepository pedidoRepository) {
        this.pedidoRepository = pedidoRepository;
    }

    /* ===== CRUD BÁSICO ===== */

    public List<Pedido> listarTodos() {
        return pedidoRepository.findAll();
    }

    public Optional<Pedido> findById(Long id) {
        return pedidoRepository.findById(id);
    }

    @Transactional
    public Pedido salvar(Pedido pedido) {
        if (pedido.getDataCriacao() == null) {
            pedido.setDataCriacao(LocalDateTime.now());
        }
        if (pedido.getStatus() == null) {
            pedido.setStatus(StatusPedido.NOVO);
        }
        return pedidoRepository.save(pedido);
    }

    @Transactional
    public Pedido atualizar(Pedido pedido) {
        return pedidoRepository.save(pedido);
    }

    @Transactional
    public void excluir(Long id) {
        pedidoRepository.deleteById(id);
    }

    /* ===== MUDANÇA DE STATUS ===== */

    @Transactional
    protected Pedido alterarStatus(Long id, StatusPedido novoStatus) {
        Pedido pedido = pedidoRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Pedido não encontrado: " + id));
        pedido.setStatus(novoStatus);
        return pedidoRepository.save(pedido);
    }

    @Transactional
    public Pedido marcarEmAvaliacao(Long id) {
        return alterarStatus(id, StatusPedido.EM_AVALIACAO);
    }

    @Transactional
    public Pedido aprovar(Long id) {
        return alterarStatus(id, StatusPedido.APROVADO);
    }

    @Transactional
    public Pedido reprovar(Long id) {
        return alterarStatus(id, StatusPedido.REPROVADO);
    }

    @Transactional
    public Pedido executar(Long id) {
        return alterarStatus(id, StatusPedido.EM_EXECUCAO);
    }

    @Transactional
    public Pedido cancelar(Long id) {
        return alterarStatus(id, StatusPedido.CANCELADO);
    }
}
