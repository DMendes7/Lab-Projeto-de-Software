package com.carrental.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.provisioning.InMemoryUserDetailsManager;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
public class WebSecurityConfig {

    @Bean
    PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    UserDetailsService userDetailsService(PasswordEncoder encoder) {
        InMemoryUserDetailsManager users = new InMemoryUserDetailsManager();

        users.createUser(
            User.withUsername("admingia")
                .password(encoder.encode("root"))
                .roles("ADMIN")
                .build()
        );
        users.createUser(
            User.withUsername("alice@demo.com")
                .password(encoder.encode("123"))
                .roles("CLIENT")
                .build()
        );
        users.createUser(
            User.withUsername("bruno@demo.com")
                .password(encoder.encode("123"))
                .roles("CLIENT")
                .build()
        );
        return users;
    }

    @Bean
    SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.ignoringRequestMatchers("/h2/**"))
            .headers(h -> h.frameOptions(f -> f.sameOrigin()))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/", "/login", "/h2/**", "/css/**", "/js/**", "/images/**", "/fragments/**").permitAll()
                .requestMatchers("/contratantes/**", "/automoveis/**").hasRole("ADMIN")
                .requestMatchers("/pedidos/**").authenticated()
                .anyRequest().authenticated()
            )
            .formLogin(form -> form
                .loginPage("/login")
                .defaultSuccessUrl("/", true)
                .permitAll()
            )
            .logout(logout -> logout
                .logoutUrl("/logout")
                .logoutSuccessUrl("/login?logout")
                .permitAll()
            );
        return http.build();
    }
}
