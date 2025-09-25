package com.carrental.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "contratantes")
public class Contratante {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String nome;

    @Column(nullable = false, unique = true)
    private String documento;

    @Column(nullable = false, unique = true)
    private String email;

    private String endereco;
    private String profissao;
    private String rg;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private UserRole role; // ADMIN | CLIENT

    @Column(name = "senha_hash", nullable = false)
    private String senhaHash;

    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;

    // --- Getters/Setters ---

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getNome() { return nome; }
    public void setNome(String nome) { this.nome = nome; }

    public String getDocumento() { return documento; }
    public void setDocumento(String documento) { this.documento = documento; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public String getEndereco() { return endereco; }
    public void setEndereco(String endereco) { this.endereco = endereco; }

    public String getProfissao() { return profissao; }
    public void setProfissao(String profissao) { this.profissao = profissao; }

    public String getRg() { return rg; }
    public void setRg(String rg) { this.rg = rg; }

    public UserRole getRole() { return role; }
    public void setRole(UserRole role) { this.role = role; }

    public String getSenhaHash() { return senhaHash; }
    public void setSenhaHash(String senhaHash) { this.senhaHash = senhaHash; }

    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}
