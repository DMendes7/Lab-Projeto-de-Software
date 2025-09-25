package com.carrental.service;

import com.carrental.model.Contratante;
import com.carrental.model.UserRole;
import com.carrental.repository.ContratanteRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class ContratanteService {

    private final ContratanteRepository repository;

    public ContratanteService(ContratanteRepository repository) {
        this.repository = repository;
    }

    /** Lista todos os contratantes */
    public List<Contratante> listarTodos() {
        return repository.findAll();
    }

    /** Lista apenas usuários com perfil CLIENT */
    public List<Contratante> listarTodosClientes() {
        return repository.findAll()
                .stream()
                .filter(c -> c.getRole() == UserRole.CLIENT)
                .collect(Collectors.toList());
    }

    /** Busca por ID */
    public Optional<Contratante> buscarPorId(Long id) {
        return repository.findById(id);
    }

    /** Busca por e-mail (case-insensitive) sem depender de método custom do repositório */
    public Optional<Contratante> buscarPorEmail(String email) {
        if (email == null) return Optional.empty();
        return repository.findAll()
                .stream()
                .filter(c -> email.equalsIgnoreCase(c.getEmail()))
                .findFirst();
    }

    /** Cria/atualiza */
    @Transactional
    public Contratante salvar(Contratante c) {
        return repository.save(c);
    }

    /** Exclui por ID (nome usado no controller) */
    @Transactional
    public void excluir(Long id) {
        repository.deleteById(id);
    }

    /** Alias caso algum outro ponto do código chame deleteById */
    @Transactional
    public void deleteById(Long id) {
        excluir(id);
    }
}
