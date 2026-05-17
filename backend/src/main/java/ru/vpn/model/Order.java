package ru.vpn.model;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;

@Entity
@Table(name = "orders")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private Long userId;

    private Long tariffId;

    private Long telegramId;

    private String username;

    private String tariffName;

    private Integer price;

    private String paymentUrl;

    private String paymentMethod;

    private String status;

    @Builder.Default
    private LocalDateTime startDate = LocalDateTime.now();

    private LocalDateTime endDate;

    private LocalDateTime paidAt;
}
