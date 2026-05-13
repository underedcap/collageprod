package ru.vpn.controller;

import lombok.Data;
import org.springframework.web.bind.annotation.*;
import ru.vpn.model.Order;
import ru.vpn.model.Tariff;
import ru.vpn.model.User;
import ru.vpn.repository.OrderRepository;
import ru.vpn.repository.TariffRepository;
import ru.vpn.repository.UserRepository;

import java.time.Duration;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api")
public class BotController {

    private final UserRepository userRepo;
    private final TariffRepository tariffRepo;
    private final OrderRepository orderRepo;

    public BotController(UserRepository userRepo, TariffRepository tariffRepo, OrderRepository orderRepo) {
        this.userRepo = userRepo;
        this.tariffRepo = tariffRepo;
        this.orderRepo = orderRepo;
    }

    @GetMapping("/tariffs")
    public List<Tariff> getTariffs() {
        return tariffRepo.findAll();
    }

    @PostMapping("/orders/create")
    public String createOrder(@RequestBody OrderRequest req) {
        User user = userRepo.findByTelegramId(req.getTelegramId());
        if (user == null) {
            user = User.builder()
                    .telegramId(req.getTelegramId())
                    .username(req.getUsername())
                    .balance(0)
                    .build();
            userRepo.save(user);
        }

        Tariff tariff = tariffRepo.findByName(req.getTariffName());
        if (tariff == null) return "❌ Тариф не найден";

        LocalDateTime now = LocalDateTime.now();

        Order order = Order.builder()
                .userId(user.getId())
                .tariffId(tariff.getId())
                .status("ACTIVE")
                .startDate(now)
                .endDate(now.plusDays(tariff.getDurationDays()))
                .build();
        orderRepo.save(order);

        return "✅ Заказ создан";
    }


    @GetMapping("/orders/user/{telegramId}")
    public List<Order> getUserOrders(@PathVariable Long telegramId) {
        User user = userRepo.findByTelegramId(telegramId);
        if (user == null) return List.of();
        return orderRepo.findByUserId(user.getId());
    }


    @GetMapping("/profile/{telegramId}")
    public ProfileResponse getProfile(@PathVariable Long telegramId) {
        User user = userRepo.findByTelegramId(telegramId);
        if (user == null) {
            return new ProfileResponse("❌ Пользователь не найден");
        }

        List<Order> orders = orderRepo.findByUserId(user.getId());
        Optional<Order> activeOrder = orders.stream()
                .filter(o -> o.getStatus().equals("ACTIVE") && o.getEndDate().isAfter(LocalDateTime.now()))
                .findFirst();

        ProfileResponse resp = new ProfileResponse();
        resp.setUsername(user.getUsername());
        resp.setTelegramId(user.getTelegramId());
        resp.setBalance(user.getBalance());

        if (activeOrder.isPresent()) {
            Order order = activeOrder.get();
            Tariff tariff = tariffRepo.findById(order.getTariffId()).orElse(null);
            if (tariff != null) {
                resp.setActiveTariff(tariff.getName());
                long daysLeft = Duration.between(LocalDateTime.now(), order.getEndDate()).toDays();
                resp.setDaysLeft(daysLeft);
            }
        }

        return resp;
    }

    // реквест для создания заказа
    @Data
    public static class OrderRequest {
        private Long telegramId;
        private String username;
        private String tariffName;
    }

    @Data
    public static class ProfileResponse {
        private String status = "OK";
        private String username;
        private Long telegramId;
        private int balance;
        private String activeTariff;
        private Long daysLeft;
        private String error;

        public ProfileResponse() {}

        public ProfileResponse(String error) {
            this.status = "ERROR";
            this.error = error;
        }
    }
}