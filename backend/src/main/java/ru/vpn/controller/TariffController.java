package ru.vpn.controller;

import lombok.RequiredArgsConstructor;

import org.springframework.web.bind.annotation.*;

import ru.vpn.entity.Tariff;
import ru.vpn.repository.TariffRepository;

import java.util.List;

@RestController
@RequestMapping("/tariffs")
@RequiredArgsConstructor
public class TariffController {

    private final TariffRepository tariffRepository;

    @GetMapping
    public List<Tariff> getTariffs() {

        return tariffRepository.findAll();
    }
}