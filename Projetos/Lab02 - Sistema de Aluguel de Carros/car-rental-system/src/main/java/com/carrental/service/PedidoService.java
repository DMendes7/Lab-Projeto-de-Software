package com.carrental.service;

import com.carrental.model.Pedido;
import com.carrental.repository.PedidoRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
public class PedidoService {

    private final PedidoRepository pedidoRepository;

    public PedidoService(PedidoRepository pedidoRepository) {
        this.pedidoRepository = pedidoRepository;
    }

    // Lista todos os pedidos (ADMIN)
    @Transactional(readOnly = true)
    public List<Pedido> listarTodos() {
        return pedidoRepository.findAll();
    }

    // Lista pedidos por contratante (CLIENTE)
    @Transactional(readOnly = true)
    public List<Pedido> listarPorContratanteId(Long contratanteId) {
        return pedidoRepository.findByContratanteId(contratanteId);
    }

    // Busca por id
    @Transactional(readOnly = true)
    public Optional<Pedido> buscarPorId(Long id) {
        return pedidoRepository.findById(id);
    }

    // Cria/atualiza
    @Transactional
    public Pedido salvar(Pedido pedido) {
        return pedidoRepository.save(pedido);
    }

    // Exclui por id (método que faltava)
    @Transactional
    public void excluir(Long id) {
        pedidoRepository.deleteById(id);
    }
}
