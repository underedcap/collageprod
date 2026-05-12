package ru.vpn.entity;

import jakarta.persistence.*;

import lombok.Data;

@Entity
@Table(name = "tariffs")
@Data
public class Tariff {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;

    private Integer price;

    private Integer durationDays;
}