package com.carrental.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.ViewControllerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addViewControllers(ViewControllerRegistry registry) {
        // GET /login -> templates/login.html
        registry.addViewController("/login").setViewName("login");
        // (opcional) uma view simples de erro genérica se quiser:
        // registry.addViewController("/error").setViewName("error");
    }
}
