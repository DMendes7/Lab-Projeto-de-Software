package com.carrental.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Entity
public class Pedido {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @NotNull(message = "Data início é obrigatória")
    private LocalDate periodoInicio;
    
    @NotNull(message = "Data fim é obrigatória")
    private LocalDate periodoFim;
    
    @Enumerated(EnumType.STRING)
    private StatusPedido status = StatusPedido.NOVO;
    
    private LocalDateTime dataCriacao = LocalDateTime.now();
    
    @ManyToOne
    @JoinColumn(name = "contratante_id")
    @NotNull(message = "Contratante é obrigatório")
    private Contratante contratante;
    
    @ManyToOne
    @JoinColumn(name = "automovel_id")
    @NotNull(message = "Automóvel é obrigatório")
    private Automovel automovel;
    
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public LocalDate getPeriodoInicio() { return periodoInicio; }
    public void setPeriodoInicio(LocalDate periodoInicio) { this.periodoInicio = periodoInicio; }
    
    public LocalDate getPeriodoFim() { return periodoFim; }
    public void setPeriodoFim(LocalDate periodoFim) { this.periodoFim = periodoFim; }
    
    public StatusPedido getStatus() { return status; }
    public void setStatus(StatusPedido status) { this.status = status; }
    
    public LocalDateTime getDataCriacao() { return dataCriacao; }
    public void setDataCriacao(LocalDateTime dataCriacao) { this.dataCriacao = dataCriacao; }
    
    public Contratante getContratante() { return contratante; }
    public void setContratante(Contratante contratante) { this.contratante = contratante; }
    
    public Automovel getAutomovel() { return automovel; }
    public void setAutomovel(Automovel automovel) { this.automovel = automovel; }
}