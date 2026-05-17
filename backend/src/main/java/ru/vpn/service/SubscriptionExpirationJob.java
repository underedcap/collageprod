package ru.vpn.service;

import jakarta.transaction.Transactional;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import ru.vpn.model.User;
import ru.vpn.repository.UserRepository;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class SubscriptionExpirationJob {

    private final UserRepository userRepository;

    public SubscriptionExpirationJob(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @Scheduled(fixedRate = 60 * 60 * 1000)
    @Transactional
    public void deactivateExpiredSubscriptions() {
        List<User> expiredUsers = userRepository
                .findByActiveSubscriptionTrueAndSubscriptionEndBefore(LocalDateTime.now());

        for (User user : expiredUsers) {
            user.setActiveSubscription(false);
        }
    }
}
