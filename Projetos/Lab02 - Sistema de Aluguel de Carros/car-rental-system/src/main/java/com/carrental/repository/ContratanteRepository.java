package com.carrental.repository;

import com.carrental.model.Contratante;
import com.carrental.model.UserRole;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface ContratanteRepository extends JpaRepository<Contratante, Long> {
    Optional<Contratante> findByEmail(String email);
    List<Contratante> findByRole(UserRole role);
}
