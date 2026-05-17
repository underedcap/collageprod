package ru.vpn.model;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;

@Entity
@Table(name = "users")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private Long telegramId;

    private String username;

    @Builder.Default
    private Boolean activeSubscription = false;

    private LocalDateTime subscriptionEnd;

    @Builder.Default
    private Integer cashback = 0;
}