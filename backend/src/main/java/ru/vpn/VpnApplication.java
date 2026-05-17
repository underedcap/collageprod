package ru.vpn;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class VpnApplication {

    public static void main(String[] args) {
        SpringApplication.run(VpnApplication.class, args);
    }
}   
