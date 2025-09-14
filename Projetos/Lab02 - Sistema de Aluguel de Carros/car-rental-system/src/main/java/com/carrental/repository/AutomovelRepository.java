package com.carrental.repository;

import com.carrental.model.Automovel;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface AutomovelRepository extends JpaRepository<Automovel, Long> {
    List<Automovel> findByAtivoTrue();
}