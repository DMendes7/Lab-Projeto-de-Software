package com.carrental.service;

import com.carrental.model.Contratante;
import com.carrental.model.UserRole;
import com.carrental.repository.ContratanteRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class ContratanteService {

    private final ContratanteRepository repo;

    public ContratanteService(ContratanteRepository repo) {
        this.repo = repo;
    }

    public List<Contratante> listarTodos() {
        return repo.findAll();
    }

    /** Apenas clientes (não inclui ADMIN). */
    public List<Contratante> listarTodosClientes() {
        return repo.findByRole(UserRole.CLIENT);
    }

    public Optional<Contratante> buscarPorId(Long id) {
        return repo.findById(id);
    }

    public Optional<Contratante> buscarPorEmail(String email) {
        return repo.findByEmail(email);
    }

    public Contratante salvar(Contratante c) {
        return repo.save(c);
    }

    public void deleteById(Long id) {
        repo.deleteById(id);
    }
}
