package com.carrental.service;

import com.carrental.model.Automovel;
import com.carrental.repository.AutomovelRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class AutomovelService {

    private final AutomovelRepository repository;

    public AutomovelService(AutomovelRepository repository) {
        this.repository = repository;
    }

    /* ---------------- Compatibilidade (EN + PT) ---------------- */

    // EN
    public List<Automovel> findAll() { return repository.findAll(); }

    public Optional<Automovel> findById(Long id) { return repository.findById(id); }

    public Automovel save(Automovel a) { return repository.save(a); }

    public void deleteById(Long id) { repository.deleteById(id); }

    // PT (aliases)
    public List<Automovel> listarTodos() { return findAll(); }
    public Optional<Automovel> buscarPorId(Long id) { return findById(id); }
    public Automovel salvar(Automovel a) { return save(a); }
    public void excluir(Long id) { deleteById(id); }
}
