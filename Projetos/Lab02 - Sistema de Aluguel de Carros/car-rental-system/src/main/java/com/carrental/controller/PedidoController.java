package com.carrental.controller;

import com.carrental.model.Pedido;
import com.carrental.model.StatusPedido;
import com.carrental.service.AutomovelService;
import com.carrental.service.ContratanteService;
import com.carrental.service.PedidoService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.util.Optional;

@Controller
public class PedidoController {

    private final PedidoService pedidoService;
    private final AutomovelService automovelService;
    private final ContratanteService contratanteService;

    public PedidoController(PedidoService pedidoService,
                            AutomovelService automovelService,
                            ContratanteService contratanteService) {
        this.pedidoService = pedidoService;
        this.automovelService = automovelService;
        this.contratanteService = contratanteService;
    }

    /* =========================
       LISTA
       ========================= */
    @GetMapping("/pedidos")
    public String listar(Model model,
                         @RequestParam(value = "success", required = false) String success,
                         @RequestParam(value = "error", required = false) String error) {

        model.addAttribute("pedidos", pedidoService.listarTodos());

        if (success != null) model.addAttribute("successMessage", success);
        if (error != null) model.addAttribute("errorMessage", error);

        return "pedido-list";
    }

    /* =========================
       DETALHES
       ========================= */
    @GetMapping("/pedidos/{id}")
    public String detalhes(@PathVariable Long id, Model model, RedirectAttributes ra) {
        Optional<Pedido> opt = pedidoService.findById(id);
        if (opt.isEmpty()) {
            ra.addFlashAttribute("errorMessage", "Pedido não encontrado.");
            return "redirect:/pedidos";
        }
        model.addAttribute("pedido", opt.get());
        return "pedido-detalhe";
    }

    /* =========================
       NOVO / SALVAR
       ========================= */
    @GetMapping("/pedidos/novo")
    public String novo(Model model) {
        model.addAttribute("pedido", new Pedido());
        model.addAttribute("contratantes", contratanteService.listarTodos());
        model.addAttribute("automoveis", automovelService.listarTodos());
        model.addAttribute("status", StatusPedido.values());
        return "pedido-form";
    }

    @PostMapping("/pedidos/salvar")
    public String salvar(@ModelAttribute Pedido pedido, RedirectAttributes ra) {
        try {
            pedidoService.salvar(pedido);
            ra.addFlashAttribute("successMessage", "Pedido cadastrado com sucesso.");
            return "redirect:/pedidos";
        } catch (Exception e) {
            ra.addFlashAttribute("errorMessage", "Erro ao salvar: " + e.getMessage());
            return "redirect:/pedidos/novo";
        }
    }

    /* =========================
       EDITAR / ATUALIZAR
       ========================= */
    @GetMapping("/pedidos/editar/{id}")
    public String editar(@PathVariable Long id, Model model, RedirectAttributes ra) {
        Optional<Pedido> opt = pedidoService.findById(id);
        if (opt.isEmpty()) {
            ra.addFlashAttribute("errorMessage", "Pedido não encontrado.");
            return "redirect:/pedidos";
        }
        model.addAttribute("pedido", opt.get());
        model.addAttribute("contratantes", contratanteService.listarTodos());
        model.addAttribute("automoveis", automovelService.listarTodos());
        model.addAttribute("status", StatusPedido.values());
        return "pedido-form";
    }

    @PostMapping("/pedidos/atualizar")
    public String atualizar(@ModelAttribute Pedido pedido, RedirectAttributes ra) {
        try {
            pedidoService.atualizar(pedido);
            ra.addFlashAttribute("successMessage", "Pedido atualizado com sucesso.");
            return "redirect:/pedidos/{id}".replace("{id}", String.valueOf(pedido.getId())); // volta aos detalhes
        } catch (Exception e) {
            ra.addFlashAttribute("errorMessage", "Erro ao atualizar: " + e.getMessage());
            return "redirect:/pedidos/editar/" + pedido.getId();
        }
    }

    /* =========================
       EXCLUIR
       ========================= */
    @GetMapping("/pedidos/excluir/{id}")
    public String excluir(@PathVariable Long id, RedirectAttributes ra) {
        try {
            pedidoService.excluir(id);
            ra.addFlashAttribute("successMessage", "Pedido excluído com sucesso.");
        } catch (Exception e) {
            ra.addFlashAttribute("errorMessage", "Erro ao excluir: " + e.getMessage());
        }
        return "redirect:/pedidos";
    }

    /* =========================
       AÇÕES DE STATUS
       ========================= */
    @GetMapping("/pedidos/cancelar/{id}")
    public String cancelar(@PathVariable Long id, RedirectAttributes ra) {
        try {
            pedidoService.cancelar(id);
            ra.addFlashAttribute("successMessage", "Pedido cancelado.");
        } catch (Exception e) {
            ra.addFlashAttribute("errorMessage", "Erro ao cancelar: " + e.getMessage());
        }
        return "redirect:/pedidos/" + id;
    }

    @GetMapping("/pedidos/aprovar/{id}")
    public String aprovar(@PathVariable Long id, RedirectAttributes ra) {
        try {
            pedidoService.aprovar(id);
            ra.addFlashAttribute("successMessage", "Pedido aprovado.");
        } catch (Exception e) {
            ra.addFlashAttribute("errorMessage", "Erro ao aprovar: " + e.getMessage());
        }
        return "redirect:/pedidos/" + id;
    }

    @GetMapping("/pedidos/reprovar/{id}")
    public String reprovar(@PathVariable Long id, RedirectAttributes ra) {
        try {
            pedidoService.reprovar(id);
            ra.addFlashAttribute("successMessage", "Pedido reprovado.");
        } catch (Exception e) {
            ra.addFlashAttribute("errorMessage", "Erro ao reprovar: " + e.getMessage());
        }
        return "redirect:/pedidos/" + id;
    }

    @GetMapping("/pedidos/executar/{id}")
    public String executar(@PathVariable Long id, RedirectAttributes ra) {
        try {
            pedidoService.executar(id);
            ra.addFlashAttribute("successMessage", "Pedido colocado em execução.");
        } catch (Exception e) {
            ra.addFlashAttribute("errorMessage", "Erro ao executar: " + e.getMessage());
        }
        return "redirect:/pedidos/" + id;
    }
}
