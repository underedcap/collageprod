package ru.vpn.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.vpn.model.Tariff;

public interface TariffRepository extends JpaRepository<Tariff, Long> {
    Tariff findByName(String name);
}