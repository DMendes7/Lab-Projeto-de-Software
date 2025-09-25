package com.carrental.controller;

import com.carrental.model.Automovel;
import com.carrental.model.Contratante;
import com.carrental.model.Pedido;
import com.carrental.model.StatusPedido;
import com.carrental.service.AutomovelService;
import com.carrental.service.ContratanteService;
import com.carrental.service.PedidoService;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Controller
@RequestMapping("/pedidos")
public class PedidoController {

    private final PedidoService pedidoService;
    private final ContratanteService contratanteService;
    private final AutomovelService automovelService;

    public PedidoController(PedidoService pedidoService,
                            ContratanteService contratanteService,
                            AutomovelService automovelService) {
        this.pedidoService = pedidoService;
        this.contratanteService = contratanteService;
        this.automovelService = automovelService;
    }

    // ======================
    // LISTAGEM
    // ======================
    @GetMapping
    public String listar(Model model, Authentication auth, RedirectAttributes ra) {
        try {
            boolean isAdmin = auth != null && auth.getAuthorities().stream()
                    .anyMatch(a -> a.getAuthority().equals("ROLE_ADMIN"));

            List<Pedido> pedidos;
            if (isAdmin) {
                pedidos = pedidoService.listarTodos();
            } else {
                String email = (auth != null) ? auth.getName() : null;
                if (email == null) {
                    ra.addFlashAttribute("errorMessage", "Sessão expirada. Faça login novamente.");
                    return "redirect:/login";
                }
                Optional<Contratante> oc = contratanteService.buscarPorEmail(email);
                if (oc.isEmpty()) {
                    ra.addFlashAttribute("errorMessage", "Usuário não encontrado.");
                    return "redirect:/login";
                }
                pedidos = pedidoService.listarPorContratanteId(oc.get().getId());
            }

            model.addAttribute("pedidos", pedidos);
            return "pedido-list";
        } catch (Exception e) {
            ra.addFlashAttribute("errorMessage", "Erro ao carregar pedidos: " + e.getMessage());
            return "redirect:/";
        }
    }

    // ======================
    // DETALHE
    // ======================
    @GetMapping("/{id}")
    public String detalhes(@PathVariable Long id,
                           Model model,
                           Authentication auth,
                           RedirectAttributes ra) {
        Optional<Pedido> opt = pedidoService.buscarPorId(id);
        if (opt.isEmpty()) {
            ra.addFlashAttribute("errorMessage", "Pedido não encontrado.");
            return "redirect:/pedidos";
        }
        Pedido pedido = opt.get();

        boolean isAdmin = auth != null && auth.getAuthorities().stream()
                .anyMatch(a -> a.getAuthority().equals("ROLE_ADMIN"));

        if (!isAdmin) {
            String emailLogado = auth != null ? auth.getName() : null;
            String emailPedido = (pedido.getContratante() != null) ? pedido.getContratante().getEmail() : null;
            if (emailLogado == null || emailPedido == null || !emailLogado.equalsIgnoreCase(emailPedido)) {
                ra.addFlashAttribute("errorMessage", "Você não tem permissão para ver este pedido.");
                return "redirect:/pedidos";
            }
        }

        model.addAttribute("pedido", pedido);
        return "pedido-detalhe";
    }

    // ======================
    // NOVO
    // ======================
    @GetMapping("/novo")
    public String novo(Model model, Authentication auth, RedirectAttributes ra) {
        Pedido pedido = new Pedido();
        pedido.setStatus(StatusPedido.NOVO);
        pedido.setDataCriacao(LocalDateTime.now());

        popularSelects(model, auth);
        model.addAttribute("pedido", pedido);
        return "pedido-form";
    }

    // ======================
    // EDITAR
    // ======================
    @GetMapping("/editar/{id}")
    public String editar(@PathVariable Long id, Model model, Authentication auth, RedirectAttributes ra) {
        Optional<Pedido> opt = pedidoService.buscarPorId(id);
        if (opt.isEmpty()) {
            ra.addFlashAttribute("errorMessage", "Pedido não encontrado.");
            return "redirect:/pedidos";
        }
        Pedido pedido = opt.get();

        boolean isAdmin = auth != null && auth.getAuthorities().stream()
                .anyMatch(a -> a.getAuthority().equals("ROLE_ADMIN"));

        if (!isAdmin) {
            String emailLogado = auth != null ? auth.getName() : null;
            String emailPedido = (pedido.getContratante() != null) ? pedido.getContratante().getEmail() : null;
            if (emailLogado == null || emailPedido == null || !emailLogado.equalsIgnoreCase(emailPedido)) {
                ra.addFlashAttribute("errorMessage", "Você não tem permissão para editar este pedido.");
                return "redirect:/pedidos";
            }
        }

        popularSelects(model, auth);
        model.addAttribute("pedido", pedido);
        return "pedido-form";
    }

    // ======================
    // SALVAR (CRIAR/ATUALIZAR)
    // ======================
    @PostMapping("/salvar")
    public String salvar(@ModelAttribute Pedido form,
                         Authentication auth,
                         RedirectAttributes ra) {
        try {
            // Resolver relacionamento Contratante
            Long contratanteId = (form.getContratante() != null) ? form.getContratante().getId() : null;
            Contratante contratante = (contratanteId != null)
                    ? contratanteService.buscarPorId(contratanteId).orElse(null)
                    : null;

            // Resolver relacionamento Automovel
            Long automovelId = (form.getAutomovel() != null) ? form.getAutomovel().getId() : null;
            Automovel automovel = (automovelId != null)
                    ? automovelService.buscarPorId(automovelId).orElse(null)
                    : null;

            boolean isAdmin = auth != null && auth.getAuthorities().stream()
                    .anyMatch(a -> a.getAuthority().equals("ROLE_ADMIN"));

            if (form.getId() == null) {
                // Novo
                Pedido novo = new Pedido();
                novo.setContratante(contratante);
                novo.setAutomovel(automovel);
                novo.setPeriodoInicio(form.getPeriodoInicio());
                novo.setPeriodoFim(form.getPeriodoFim());
                // se vier status do form e for admin, respeita; senão NOVO
                if (isAdmin && form.getStatus() != null) {
                    novo.setStatus(form.getStatus());
                } else {
                    novo.setStatus(StatusPedido.NOVO);
                }
                novo.setDataCriacao(LocalDateTime.now());
                pedidoService.salvar(novo);
                ra.addFlashAttribute("successMessage", "Pedido criado com sucesso!");
            } else {
                // Update
                Pedido db = pedidoService.buscarPorId(form.getId())
                        .orElseThrow(() -> new IllegalArgumentException("Pedido não encontrado"));

                // Restrição: cliente só pode editar o próprio
                if (!isAdmin) {
                    String emailLogado = auth != null ? auth.getName() : null;
                    String emailPedido = (db.getContratante() != null) ? db.getContratante().getEmail() : null;
                    if (emailLogado == null || emailPedido == null || !emailLogado.equalsIgnoreCase(emailPedido)) {
                        ra.addFlashAttribute("errorMessage", "Você não tem permissão para editar este pedido.");
                        return "redirect:/pedidos";
                    }
                }

                db.setContratante(contratante);
                db.setAutomovel(automovel);
                db.setPeriodoInicio(form.getPeriodoInicio());
                db.setPeriodoFim(form.getPeriodoFim());
                if (isAdmin && form.getStatus() != null) {
                    db.setStatus(form.getStatus());
                }
                // dataCriacao permanece
                pedidoService.salvar(db);
                ra.addFlashAttribute("successMessage", "Pedido atualizado com sucesso!");
            }

            return "redirect:/pedidos";
        } catch (Exception e) {
            ra.addFlashAttribute("errorMessage", "Falha ao salvar pedido: " + e.getMessage());
            return "redirect:/pedidos";
        }
    }

    // ======================
    // EXCLUIR
    // ======================
    @GetMapping("/excluir/{id}")
    public String excluir(@PathVariable Long id, Authentication auth, RedirectAttributes ra) {
        try {
            Pedido p = pedidoService.buscarPorId(id)
                    .orElseThrow(() -> new IllegalArgumentException("Pedido não encontrado"));

            boolean isAdmin = auth != null && auth.getAuthorities().stream()
                    .anyMatch(a -> a.getAuthority().equals("ROLE_ADMIN"));

            if (!isAdmin) {
                String emailLogado = auth != null ? auth.getName() : null;
                String emailPedido = (p.getContratante() != null) ? p.getContratante().getEmail() : null;
                if (emailLogado == null || emailPedido == null || !emailLogado.equalsIgnoreCase(emailPedido)) {
                    ra.addFlashAttribute("errorMessage", "Você não tem permissão para excluir este pedido.");
                    return "redirect:/pedidos";
                }
            }

            pedidoService.excluir(id);
            ra.addFlashAttribute("successMessage", "Pedido excluído com sucesso!");
        } catch (Exception e) {
            ra.addFlashAttribute("errorMessage", "Falha ao excluir pedido: " + e.getMessage());
        }
        return "redirect:/pedidos";
    }

    // ======================
    // AÇÕES DE STATUS
    // ======================
    @GetMapping("/cancelar/{id}")
    public String cancelar(@PathVariable Long id, Authentication auth, RedirectAttributes ra) {
        try {
            Pedido p = pedidoService.buscarPorId(id)
                    .orElseThrow(() -> new IllegalArgumentException("Pedido não encontrado"));

            boolean isAdmin = auth != null && auth.getAuthorities().stream()
                    .anyMatch(a -> a.getAuthority().equals("ROLE_ADMIN"));

            // cliente só o próprio
            if (!isAdmin) {
                String emailLogado = auth != null ? auth.getName() : null;
                String emailPedido = (p.getContratante() != null) ? p.getContratante().getEmail() : null;
                if (emailLogado == null || emailPedido == null || !emailLogado.equalsIgnoreCase(emailPedido)) {
                    ra.addFlashAttribute("errorMessage", "Você não tem permissão para cancelar este pedido.");
                    return "redirect:/pedidos";
                }
            }

            if (p.getStatus() == StatusPedido.NOVO || p.getStatus() == StatusPedido.EM_AVALIACAO) {
                p.setStatus(StatusPedido.CANCELADO);
                pedidoService.salvar(p);
                ra.addFlashAttribute("successMessage", "Pedido cancelado.");
            } else {
                ra.addFlashAttribute("errorMessage", "Este pedido não pode ser cancelado no status atual.");
            }
        } catch (Exception e) {
            ra.addFlashAttribute("errorMessage", "Falha ao cancelar: " + e.getMessage());
        }
        return "redirect:/pedidos";
    }

    @GetMapping("/aprovar/{id}")
    public String aprovar(@PathVariable Long id, Authentication auth, RedirectAttributes ra) {
        if (!isAdmin(auth)) {
            ra.addFlashAttribute("errorMessage", "Apenas administradores podem aprovar pedidos.");
            return "redirect:/pedidos";
        }
        try {
            Pedido p = pedidoService.buscarPorId(id)
                    .orElseThrow(() -> new IllegalArgumentException("Pedido não encontrado"));
            p.setStatus(StatusPedido.APROVADO);
            pedidoService.salvar(p);
            ra.addFlashAttribute("successMessage", "Pedido aprovado.");
        } catch (Exception e) {
            ra.addFlashAttribute("errorMessage", "Falha ao aprovar: " + e.getMessage());
        }
        return "redirect:/pedidos/" + id;
    }

    @GetMapping("/reprovar/{id}")
    public String reprovar(@PathVariable Long id, Authentication auth, RedirectAttributes ra) {
        if (!isAdmin(auth)) {
            ra.addFlashAttribute("errorMessage", "Apenas administradores podem reprovar pedidos.");
            return "redirect:/pedidos";
        }
        try {
            Pedido p = pedidoService.buscarPorId(id)
                    .orElseThrow(() -> new IllegalArgumentException("Pedido não encontrado"));
            p.setStatus(StatusPedido.REPROVADO);
            pedidoService.salvar(p);
            ra.addFlashAttribute("successMessage", "Pedido reprovado.");
        } catch (Exception e) {
            ra.addFlashAttribute("errorMessage", "Falha ao reprovar: " + e.getMessage());
        }
        return "redirect:/pedidos/" + id;
    }

    @GetMapping("/executar/{id}")
    public String executar(@PathVariable Long id, Authentication auth, RedirectAttributes ra) {
        if (!isAdmin(auth)) {
            ra.addFlashAttribute("errorMessage", "Apenas administradores podem iniciar a execução.");
            return "redirect:/pedidos";
        }
        try {
            Pedido p = pedidoService.buscarPorId(id)
                    .orElseThrow(() -> new IllegalArgumentException("Pedido não encontrado"));
            if (p.getStatus() == StatusPedido.APROVADO) {
                p.setStatus(StatusPedido.EM_EXECUCAO);
                pedidoService.salvar(p);
                ra.addFlashAttribute("successMessage", "Pedido em execução.");
            } else {
                ra.addFlashAttribute("errorMessage", "Somente pedidos aprovados podem entrar em execução.");
            }
        } catch (Exception e) {
            ra.addFlashAttribute("errorMessage", "Falha ao iniciar execução: " + e.getMessage());
        }
        return "redirect:/pedidos/" + id;
    }

    // ======================
    // HELPERS
    // ======================
    private void popularSelects(Model model, Authentication auth) {
        boolean isAdmin = isAdmin(auth);

        List<Automovel> automoveis = automovelService.listarTodos();
        model.addAttribute("automoveis", automoveis);

        if (isAdmin) {
            model.addAttribute("contratantes", contratanteService.listarTodosClientes());
        } else {
            String email = (auth != null) ? auth.getName() : null;
            Optional<Contratante> oc = (email != null) ? contratanteService.buscarPorEmail(email) : Optional.empty();
            // para cliente, mostra apenas ele próprio no select
            model.addAttribute("contratantes", oc.map(List::of).orElse(List.of()));
        }

        model.addAttribute("statusValues", StatusPedido.values());
    }

    private boolean isAdmin(Authentication auth) {
        return auth != null && auth.getAuthorities().stream()
                .anyMatch(a -> a.getAuthority().equals("ROLE_ADMIN"));
    }
}
