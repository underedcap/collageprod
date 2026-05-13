package ru.vpn.controller;

import lombok.Data;
import org.springframework.web.bind.annotation.*;
import ru.vpn.model.Tariff;
import ru.vpn.model.User;
import ru.vpn.repository.TariffRepository;
import ru.vpn.repository.UserRepository;

import java.time.LocalDateTime;
import java.util.List;

@RestController
@RequestMapping("/api")
public class BotController {

    private final UserRepository userRepo;
    private final TariffRepository tariffRepo;

    public BotController(UserRepository userRepo, TariffRepository tariffRepo) {
        this.userRepo = userRepo;
        this.tariffRepo = tariffRepo;
    }

    // Список тарифов
    @GetMapping("/tariffs")
    public List<Tariff> getTariffs() {
        return tariffRepo.findAll();
    }

    // Создание или обновление пользователя и подписки
    @PostMapping("/users/subscribe")
    public String subscribeUser(@RequestBody SubscribeRequest req) {
        User user = userRepo.findByTelegramId(req.getTelegramId());
        if (user == null) {
            user = User.builder()
                    .telegramId(req.getTelegramId())
                    .username(req.getUsername())
                    .activeSubscription(true)
                    .subscriptionEnd(LocalDateTime.now().plusDays(req.getDurationDays()))
                    .build();
        } else {
            // обновляем подписку
            user.setActiveSubscription(true);
            user.setSubscriptionEnd(LocalDateTime.now().plusDays(req.getDurationDays()));
        }
        userRepo.save(user);

        // генерируем ссылку на оплату (заглушка)
        String paymentLink = "https://payment.fake/checkout?user=" + user.getTelegramId() + "&tariff=" + req.getTariffName();

        return paymentLink;
    }

    @GetMapping("/users/{telegramId}")
    public User getUser(@PathVariable Long telegramId) {
        return userRepo.findByTelegramId(telegramId);
    }

    @Data
    public static class SubscribeRequest {
        private Long telegramId;
        private String username;
        private String tariffName;
        private int durationDays;
    }
}