package com.carrental.security;

import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;

/**
 * Implementação mantida sem @Service para NÃO registrar este UserDetailsService
 * como bean. Assim evitamos conflito com o InMemoryUserDetailsManager definido
 * em WebSecurityConfig.
 *
 * Caso queira reativar a autenticação via banco no futuro:
 *  1) Adicione @Service nesta classe;
 *  2) Injete o ContratanteRepository;
 *  3) Implemente a busca do usuário e a criação de um UserDetails com as roles.
 */
public class CustomUserDetailsService implements UserDetailsService {

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        // Desabilitado de propósito: estamos usando usuários em memória.
        throw new UsernameNotFoundException(
            "CustomUserDetailsService desabilitado: autenticação está usando usuários em memória.");
    }
}
