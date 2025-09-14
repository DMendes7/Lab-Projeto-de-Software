package com.carrental.service;

import com.carrental.model.Automovel;
import com.carrental.repository.AutomovelRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
public class AutomovelService {

    private final AutomovelRepository automovelRepository;

    public AutomovelService(AutomovelRepository automovelRepository) {
        this.automovelRepository = automovelRepository;
    }

    /* ===== API nova (que eu havia proposto) ===== */
    public List<Automovel> listarTodos() {
        return automovelRepository.findAll();
    }

    public Optional<Automovel> findById(Long id) {
        return automovelRepository.findById(id);
    }

    @Transactional
    public Automovel salvar(Automovel a) {
        return automovelRepository.save(a);
    }

    @Transactional
    public Automovel atualizar(Automovel a) {
        return automovelRepository.save(a);
    }

    @Transactional
    public void excluir(Long id) {
        automovelRepository.deleteById(id);
    }

    /* ===== ALIASES para compatibilidade com controllers antigos ===== */
    public List<Automovel> findAll() {                 // usado no AutomovelController
        return listarTodos();
    }

    @Transactional
    public Automovel save(Automovel a) {               // usado no AutomovelController
        return salvar(a);
    }

    @Transactional
    public void deleteById(Long id) {                  // usado no AutomovelController
        excluir(id);
    }

    @Transactional
    public Automovel update(Automovel a) {             // caso algum controller chame update(...)
        return atualizar(a);
    }
}
