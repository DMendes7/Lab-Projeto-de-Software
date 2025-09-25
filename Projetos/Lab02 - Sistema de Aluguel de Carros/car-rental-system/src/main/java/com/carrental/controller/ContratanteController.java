package com.carrental.controller;

import com.carrental.model.Contratante;
import com.carrental.model.UserRole;
import com.carrental.service.ContratanteService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.util.List;

@Controller
@RequestMapping("/contratantes")
public class ContratanteController {

    private final ContratanteService contratanteService;

    public ContratanteController(ContratanteService contratanteService) {
        this.contratanteService = contratanteService;
    }

    // LISTA
    @GetMapping
    public String listar(Model model) {
        List<Contratante> contratantes = contratanteService.listarTodos();
        model.addAttribute("contratantes", contratantes);
        return "contratante-list";
    }

    // NOVO
    @GetMapping("/novo")
    public String novo(Model model) {
        model.addAttribute("contratante", new Contratante());
        model.addAttribute("roles", UserRole.values());
        return "contratante-form";
    }

    // EDITAR
    @GetMapping("/editar/{id}")
    public String editar(@PathVariable Long id, Model model) {
        Contratante c = contratanteService.buscarPorId(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Contratante não encontrado"));
        model.addAttribute("contratante", c);
        model.addAttribute("roles", UserRole.values());
        return "contratante-form";
    }

    // SALVAR (create/update)
    @PostMapping("/salvar")
    public String salvar(@Valid @ModelAttribute("contratante") Contratante form,
                         BindingResult binding,
                         RedirectAttributes ra,
                         Model model) {

        if (binding.hasErrors()) {
            // volta para o form com os mesmos atributos necessários
            model.addAttribute("roles", UserRole.values());
            return "contratante-form";
        }

        try {
            contratanteService.salvar(form);
            ra.addFlashAttribute("successMessage", "Contratante salvo com sucesso.");
            return "redirect:/contratantes";
        } catch (Exception ex) {
            model.addAttribute("roles", UserRole.values());
            model.addAttribute("errorMessage", "Erro ao salvar: " + ex.getMessage());
            return "contratante-form";
        }
    }

    // EXCLUIR
    @GetMapping("/excluir/{id}")
    public String excluir(@PathVariable Long id, RedirectAttributes ra) {
        contratanteService.excluir(id);
        ra.addFlashAttribute("successMessage", "Contratante excluído com sucesso.");
        return "redirect:/contratantes";
    }
}
