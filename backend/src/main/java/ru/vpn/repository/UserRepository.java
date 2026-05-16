package ru.vpn.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.vpn.model.User;

import java.time.LocalDateTime;
import java.util.List;

public interface UserRepository extends JpaRepository<User, Long> {
    User findByTelegramId(Long telegramId);

    List<User> findByActiveSubscriptionTrueAndSubscriptionEndBefore(LocalDateTime now);
}
