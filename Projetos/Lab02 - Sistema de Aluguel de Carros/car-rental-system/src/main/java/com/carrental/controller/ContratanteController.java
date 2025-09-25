package com.carrental.controller;

import com.carrental.model.Contratante;
import com.carrental.service.ContratanteService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.util.Optional;

@Controller
@RequestMapping("/contratantes")
public class ContratanteController {

    private final ContratanteService contratanteService;

    public ContratanteController(ContratanteService contratanteService) {
        this.contratanteService = contratanteService;
    }

    @GetMapping
    public String listar(Model model) {
        model.addAttribute("contratantes", contratanteService.listarTodos());
        return "contratante-list";
    }

    @GetMapping("/novo")
    public String novo(Model model) {
        model.addAttribute("contratante", new Contratante());
        return "contratante-form";
    }

    @GetMapping("/editar/{id}")
    public String editar(@PathVariable Long id, Model model, RedirectAttributes ra) {
        Optional<Contratante> opt = contratanteService.buscarPorId(id);
        if (opt.isEmpty()) {
            ra.addFlashAttribute("errorMessage", "Contratante não encontrado.");
            return "redirect:/contratantes";
        }
        model.addAttribute("contratante", opt.get());
        return "contratante-form";
    }

    @PostMapping("/salvar")
    public String salvar(@ModelAttribute Contratante contratante, RedirectAttributes ra) {
        contratanteService.salvar(contratante);
        ra.addFlashAttribute("successMessage", "Contratante salvo com sucesso.");
        return "redirect:/contratantes";
    }

    @GetMapping("/excluir/{id}")
    public String excluir(@PathVariable Long id, RedirectAttributes ra) {
        contratanteService.deleteById(id);
        ra.addFlashAttribute("successMessage", "Contratante excluído com sucesso.");
        return "redirect:/contratantes";
    }
}
