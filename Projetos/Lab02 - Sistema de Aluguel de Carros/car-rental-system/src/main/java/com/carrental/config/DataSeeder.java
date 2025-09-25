package com.carrental.config;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Component;

@ConditionalOnProperty(value = "app.seed.enabled", havingValue = "true", matchIfMissing = false)
@Component
public class DataSeeder implements CommandLineRunner {
    @Override
    public void run(String... args) throws Exception {
        // deixe vazio por enquanto ou com o que você já tinha
        // (não será executado enquanto app.seed.enabled=false)
    }
}
