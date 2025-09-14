package com.carrental.service;

import com.carrental.model.Contratante;
import com.carrental.repository.ContratanteRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
public class ContratanteService {

    private final ContratanteRepository contratanteRepository;

    public ContratanteService(ContratanteRepository contratanteRepository) {
        this.contratanteRepository = contratanteRepository;
    }

    /* ===== API nova (que eu havia proposto) ===== */
    public List<Contratante> listarTodos() {
        return contratanteRepository.findAll();
    }

    public Optional<Contratante> findById(Long id) {
        return contratanteRepository.findById(id);
    }

    @Transactional
    public Contratante salvar(Contratante c) {
        return contratanteRepository.save(c);
    }

    @Transactional
    public Contratante atualizar(Contratante c) {
        return contratanteRepository.save(c);
    }

    @Transactional
    public void excluir(Long id) {
        contratanteRepository.deleteById(id);
    }

    /* ===== ALIASES para compatibilidade com controllers antigos ===== */
    public List<Contratante> findAll() {               // usado no ContratanteController
        return listarTodos();
    }

    @Transactional
    public Contratante save(Contratante c) {           // usado no ContratanteController
        return salvar(c);
    }

    @Transactional
    public void deleteById(Long id) {                  // usado no ContratanteController
        excluir(id);
    }

    @Transactional
    public Contratante update(Contratante c) {         // caso algum controller chame update(...)
        return atualizar(c);
    }
}
