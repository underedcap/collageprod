package ru.vpn.controller;

import org.springframework.web.bind.annotation.*;
import ru.vpn.model.User;
import ru.vpn.repository.UserRepository;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class BotController {

    private final UserRepository userRepo;

    public BotController(UserRepository userRepo) {
        this.userRepo = userRepo;
    }

    @GetMapping("/users/{telegramId}")
    public Map<String, Object> getUser(@PathVariable Long telegramId) {
        User user = userRepo.findByTelegramId(telegramId);

        if (user == null) {
            user = User.builder()
                    .telegramId(telegramId)
                    .activeSubscription(null)
                    .cashback(0)
                    .build();

            userRepo.save(user);
        }

        Map<String, Object> response = new HashMap<>();
        response.put("activeSubscription", user.getActiveSubscription());
        response.put("subscriptionEnd", user.getSubscriptionEnd());
        response.put("cashback", user.getCashback());

        return response;
    }

    @PostMapping("/users/activate")
    public String activateSubscription(@RequestBody ActivateRequest request) {
        User user = userRepo.findByTelegramId(request.getTelegramId());

        if (user == null) {
            user = User.builder()
                    .telegramId(request.getTelegramId())
                    .username(request.getUsername())
                    .cashback(0)
                    .build();
        }

        user.setActiveSubscription(true);
        user.setSubscriptionEnd(LocalDateTime.now().plusMonths(1));

        userRepo.save(user);

        return "ok";
    }

    public static class ActivateRequest {
        private Long telegramId;
        private String username;

        public Long getTelegramId() { return telegramId; }
        public void setTelegramId(Long telegramId) { this.telegramId = telegramId; }
        public String getUsername() { return username; }
        public void setUsername(String username) { this.username = username; }
    }
}