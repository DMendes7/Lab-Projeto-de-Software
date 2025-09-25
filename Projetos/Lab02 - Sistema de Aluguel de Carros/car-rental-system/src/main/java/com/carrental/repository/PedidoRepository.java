package com.carrental.repository;

import com.carrental.model.Pedido;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface PedidoRepository extends JpaRepository<Pedido, Long> {
    List<Pedido> findByContratanteId(Long contratanteId);
}
