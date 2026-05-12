package ru.vpn.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import ru.vpn.entity.Tariff;

public interface TariffRepository
        extends JpaRepository<Tariff, Long> {
}