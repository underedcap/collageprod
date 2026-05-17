package ru.vpn.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.vpn.model.Order;

import java.util.List;

public interface OrderRepository extends JpaRepository<Order, Long> {
    List<Order> findByUserId(Long userId);

    List<Order> findTop25ByOrderByStartDateDesc();
}
