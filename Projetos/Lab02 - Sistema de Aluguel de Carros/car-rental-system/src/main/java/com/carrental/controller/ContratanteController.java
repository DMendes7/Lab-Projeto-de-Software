package com.carrental.controller;

import com.carrental.model.Contratante;
import com.carrental.service.ContratanteService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import java.util.Optional;

@Controller
@RequestMapping("/contratantes")
public class ContratanteController {
    
    @Autowired
    private ContratanteService service;
    
    @GetMapping
    public String listContratantes(Model model,
                                 @RequestParam(value = "success", required = false) Boolean success,
                                 @RequestParam(value = "error", required = false) Boolean error) {
        model.addAttribute("contratantes", service.findAll());
        
        if (Boolean.TRUE.equals(success)) {
            model.addAttribute("successMessage", "Operação realizada com sucesso!");
        }
        if (Boolean.TRUE.equals(error)) {
            model.addAttribute("errorMessage", "Erro ao realizar a operação. Tente novamente.");
        }
        
        return "contratante-list";
    }
    
    @GetMapping("/novo")
    public String showForm(Model model,
                          @RequestParam(value = "error", required = false) Boolean error) {
        model.addAttribute("contratante", new Contratante());
        
        if (Boolean.TRUE.equals(error)) {
            model.addAttribute("errorMessage", "Erro ao salvar contratante. Verifique os dados.");
        }
        
        return "contratante-form";
    }
    
    @PostMapping("/salvar")
    public String saveContratante(@ModelAttribute Contratante contratante) {
        try {
            service.save(contratante);
            return "redirect:/contratantes?success=true";
        } catch (Exception e) {
            return "redirect:/contratantes/novo?error=true";
        }
    }
    
    @GetMapping("/editar/{id}")
    public String editContratante(@PathVariable Long id, Model model) {
        Optional<Contratante> contratante = service.findById(id);
        if (contratante.isPresent()) {
            model.addAttribute("contratante", contratante.get());
            return "contratante-form";
        }
        return "redirect:/contratantes?error=true";
    }
    
    @GetMapping("/excluir/{id}")
    public String deleteContratante(@PathVariable Long id) {
        try {
            service.deleteById(id);
            return "redirect:/contratantes?success=true";
        } catch (Exception e) {
            return "redirect:/contratantes?error=true";
        }
    }
}