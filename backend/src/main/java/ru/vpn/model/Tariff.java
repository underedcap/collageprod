package ru.vpn.model;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "tariffs")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Tariff {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private int price;
    private int durationDays;
}