package com.carrental.controller;

import com.carrental.model.Automovel;
import com.carrental.service.AutomovelService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import java.util.Optional;

@Controller
@RequestMapping("/automoveis")
public class AutomovelController {
    
    @Autowired
    private AutomovelService service;
    
    @GetMapping
    public String listAutomoveis(Model model,
                               @RequestParam(value = "success", required = false) Boolean success,
                               @RequestParam(value = "error", required = false) Boolean error) {
        model.addAttribute("automoveis", service.findAll());
        
        if (Boolean.TRUE.equals(success)) {
            model.addAttribute("successMessage", "Operação realizada com sucesso!");
        }
        if (Boolean.TRUE.equals(error)) {
            model.addAttribute("errorMessage", "Erro ao realizar a operação. Tente novamente.");
        }
        
        return "automovel-list";
    }
    
    @GetMapping("/novo")
    public String showForm(Model model,
                         @RequestParam(value = "error", required = false) Boolean error) {
        model.addAttribute("automovel", new Automovel());
        
        if (Boolean.TRUE.equals(error)) {
            model.addAttribute("errorMessage", "Erro ao salvar automóvel. Verifique os dados.");
        }
        
        return "automovel-form";
    }
    
    @PostMapping("/salvar")
    public String saveAutomovel(@ModelAttribute Automovel automovel) {
        try {
            service.save(automovel);
            return "redirect:/automoveis?success=true";
        } catch (Exception e) {
            return "redirect:/automoveis/novo?error=true";
        }
    }
    
    @GetMapping("/editar/{id}")
    public String editAutomovel(@PathVariable Long id, Model model) {
        Optional<Automovel> automovel = service.findById(id);
        if (automovel.isPresent()) {
            model.addAttribute("automovel", automovel.get());
            return "automovel-form";
        }
        return "redirect:/automoveis?error=true";
    }
    
    @GetMapping("/excluir/{id}")
    public String deleteAutomovel(@PathVariable Long id) {
        try {
            service.deleteById(id);
            return "redirect:/automoveis?success=true";
        } catch (Exception e) {
            return "redirect:/automoveis?error=true";
        }
    }
}