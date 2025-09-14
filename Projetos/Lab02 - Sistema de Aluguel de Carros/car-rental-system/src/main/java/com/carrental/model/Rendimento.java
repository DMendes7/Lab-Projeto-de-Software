package com.carrental.model;

import jakarta.persistence.*;
import java.math.BigDecimal;

@Entity
public class Rendimento {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String fonte;
    private BigDecimal valorMensal;
    
    public Long getId() { 
        return id; 
    }
    
    public void setId(Long id) { 
        this.id = id; 
    }
    
    public String getFonte() { 
        return fonte; 
    }
    
    public void setFonte(String fonte) { 
        this.fonte = fonte; 
    }
    
    public BigDecimal getValorMensal() { 
        return valorMensal; 
    }
    
    public void setValorMensal(BigDecimal valorMensal) { 
        this.valorMensal = valorMensal; 
    }
}