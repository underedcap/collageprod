package ru.vpn.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.vpn.model.User;

public interface UserRepository extends JpaRepository<User, Long> {
    User findByTelegramId(Long telegramId);
}