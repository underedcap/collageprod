package ru.vpn.controller;

import org.springframework.web.bind.annotation.*;
import ru.vpn.model.Order;
import ru.vpn.model.Tariff;
import ru.vpn.model.User;
import ru.vpn.repository.OrderRepository;
import ru.vpn.repository.TariffRepository;
import ru.vpn.repository.UserRepository;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class BotController {

    private static final DateTimeFormatter SUBSCRIPTION_DATE_FORMAT =
            DateTimeFormatter.ofPattern("dd:MM:yyyy");
    private static final String DEMO_PAYMENT_URL = "https://pay.example.com/insight-vpn-demo-149";

    private final UserRepository userRepo;
    private final TariffRepository tariffRepo;
    private final OrderRepository orderRepo;

    public BotController(
            UserRepository userRepo,
            TariffRepository tariffRepo,
            OrderRepository orderRepo
    ) {
        this.userRepo = userRepo;
        this.tariffRepo = tariffRepo;
        this.orderRepo = orderRepo;
    }

    @GetMapping("/users/{telegramId}")
    public Map<String, Object> getUser(@PathVariable Long telegramId) {
        User user = userRepo.findByTelegramId(telegramId);

        if (user == null) {
            user = User.builder()
                    .telegramId(telegramId)
                    .activeSubscription(false)
                    .cashback(0)
                    .build();

            user = userRepo.save(user);
        }

        syncSubscriptionFromOrders(user);
        return buildUserResponse(user);
    }

    @PostMapping({"/users/activate", "/users/subscribe"})
    public Map<String, Object> activateSubscription(@RequestBody ActivateRequest request) {
        Order order = null;

        if (request.getOrderId() != null) {
            order = orderRepo.findById(request.getOrderId())
                    .orElseThrow(() -> new IllegalArgumentException("Order not found"));
        }

        User user = userRepo.findByTelegramId(request.getTelegramId());

        if (user == null) {
            user = User.builder()
                    .telegramId(request.getTelegramId())
                    .username(request.getUsername())
                    .cashback(0)
                    .build();
        } else if (request.getUsername() != null && !request.getUsername().isBlank()) {
            user.setUsername(request.getUsername());
        }

        int durationDays = request.getDurationDays() == null
                ? 30
                : request.getDurationDays();

        String tariffName = request.getTariffName() == null || request.getTariffName().isBlank()
                ? "1 Month"
                : request.getTariffName();

        LocalDateTime now = LocalDateTime.now();
        LocalDateTime startFrom = Boolean.TRUE.equals(user.getActiveSubscription())
                && user.getSubscriptionEnd() != null
                && user.getSubscriptionEnd().isAfter(now)
                ? user.getSubscriptionEnd()
                : now;
        LocalDateTime subscriptionEnd = startFrom.plusDays(durationDays);

        user.setActiveSubscription(true);
        user.setSubscriptionEnd(subscriptionEnd);
        user = userRepo.save(user);

        Tariff tariff = findOrCreateTariff(tariffName, durationDays, request.getPrice());

        if (order == null) {
            order = Order.builder()
                    .startDate(now)
                    .build();
        }

        order.setUserId(user.getId());
        order.setTariffId(tariff.getId());
        order.setTelegramId(user.getTelegramId());
        order.setUsername(user.getUsername());
        order.setTariffName(tariff.getName());
        order.setPrice(tariff.getPrice());
        order.setPaymentUrl(order.getPaymentUrl() == null ? DEMO_PAYMENT_URL : order.getPaymentUrl());
        if (order.getPaymentMethod() == null || order.getPaymentMethod().isBlank()) {
            order.setPaymentMethod(normalizePaymentMethod(request.getPaymentMethod()));
        }
        order.setStatus("PAID");
        order.setEndDate(subscriptionEnd);
        order.setPaidAt(now);
        orderRepo.save(order);

        Map<String, Object> response = buildUserResponse(user);
        response.put("status", "ok");
        response.put("orderStatus", "PAID");
        response.put("orderId", order.getId());

        return response;
    }

    @PostMapping("/orders/create")
    public Map<String, Object> createPaymentOrder(@RequestBody ActivateRequest request) {
        User user = userRepo.findByTelegramId(request.getTelegramId());

        if (user == null) {
            user = User.builder()
                    .telegramId(request.getTelegramId())
                    .username(request.getUsername())
                    .activeSubscription(false)
                    .cashback(0)
                    .build();
        } else if (request.getUsername() != null && !request.getUsername().isBlank()) {
            user.setUsername(request.getUsername());
        }

        user = userRepo.save(user);

        int durationDays = request.getDurationDays() == null ? 30 : request.getDurationDays();
        String tariffName = request.getTariffName() == null || request.getTariffName().isBlank()
                ? "1 Month"
                : request.getTariffName();
        Tariff tariff = findOrCreateTariff(tariffName, durationDays, request.getPrice());

        Order order = orderRepo.save(Order.builder()
                .userId(user.getId())
                .tariffId(tariff.getId())
                .telegramId(user.getTelegramId())
                .username(user.getUsername())
                .tariffName(tariff.getName())
                .price(tariff.getPrice())
                .paymentUrl(DEMO_PAYMENT_URL)
                .paymentMethod(normalizePaymentMethod(request.getPaymentMethod()))
                .status("PENDING")
                .startDate(LocalDateTime.now())
                .build());

        Map<String, Object> response = new HashMap<>();
        response.put("orderId", order.getId());
        response.put("status", order.getStatus());
        response.put("paymentUrl", order.getPaymentUrl());
        response.put("paymentMethod", order.getPaymentMethod());
        response.put("tariffName", order.getTariffName());
        response.put("price", order.getPrice());

        return response;
    }

    @GetMapping("/orders/recent")
    public List<Order> getRecentOrders() {
        return orderRepo.findTop25ByOrderByStartDateDesc();
    }

    private Tariff findOrCreateTariff(String name, int durationDays, Integer price) {
        Tariff tariff = tariffRepo.findByName(name);

        if (tariff != null) {
            return tariff;
        }

        return tariffRepo.save(Tariff.builder()
                .name(name)
                .price(price == null ? 149 : price)
                .durationDays(durationDays)
                .build());
    }

    private void deactivateIfExpired(User user) {
        if (!Boolean.TRUE.equals(user.getActiveSubscription())) {
            return;
        }

        if (user.getSubscriptionEnd() == null || user.getSubscriptionEnd().isAfter(LocalDateTime.now())) {
            return;
        }

        user.setActiveSubscription(false);
        userRepo.save(user);
    }

    private void syncSubscriptionFromOrders(User user) {
        Order latestPaidOrder = orderRepo.findTopByTelegramIdAndStatusOrderByEndDateDesc(
                user.getTelegramId(),
                "PAID"
        );

        if (latestPaidOrder == null || latestPaidOrder.getEndDate() == null) {
            deactivateIfExpired(user);
            return;
        }

        boolean isActive = latestPaidOrder.getEndDate().isAfter(LocalDateTime.now());
        boolean changed = !isActive == Boolean.TRUE.equals(user.getActiveSubscription())
                || user.getSubscriptionEnd() == null
                || !user.getSubscriptionEnd().equals(latestPaidOrder.getEndDate());

        if (!changed) {
            return;
        }

        user.setActiveSubscription(isActive);
        user.setSubscriptionEnd(latestPaidOrder.getEndDate());
        userRepo.save(user);
    }

    private String normalizePaymentMethod(String paymentMethod) {
        if (paymentMethod == null || paymentMethod.isBlank()) {
            return "SBP";
        }

        return paymentMethod.trim().toUpperCase();
    }

    private Map<String, Object> buildUserResponse(User user) {
        Map<String, Object> response = new HashMap<>();

        response.put("activeSubscription", Boolean.TRUE.equals(user.getActiveSubscription()));
        response.put("subscriptionEnd", formatSubscriptionEnd(user.getSubscriptionEnd()));
        response.put("cashback", user.getCashback() == null ? 0 : user.getCashback());

        return response;
    }

    private String formatSubscriptionEnd(LocalDateTime subscriptionEnd) {
        if (subscriptionEnd == null) {
            return null;
        }

        return subscriptionEnd.format(SUBSCRIPTION_DATE_FORMAT);
    }

    public static class ActivateRequest {
        private Long telegramId;
        private String username;
        private String tariffName;
        private Integer durationDays;
        private Integer price;
        private Long orderId;
        private String paymentMethod;

        public Long getTelegramId() {
            return telegramId;
        }

        public void setTelegramId(Long telegramId) {
            this.telegramId = telegramId;
        }

        public String getUsername() {
            return username;
        }

        public void setUsername(String username) {
            this.username = username;
        }

        public String getTariffName() {
            return tariffName;
        }

        public void setTariffName(String tariffName) {
            this.tariffName = tariffName;
        }

        public Integer getDurationDays() {
            return durationDays;
        }

        public void setDurationDays(Integer durationDays) {
            this.durationDays = durationDays;
        }

        public Integer getPrice() {
            return price;
        }

        public void setPrice(Integer price) {
            this.price = price;
        }

        public Long getOrderId() {
            return orderId;
        }

        public void setOrderId(Long orderId) {
            this.orderId = orderId;
        }

        public String getPaymentMethod() {
            return paymentMethod;
        }

        public void setPaymentMethod(String paymentMethod) {
            this.paymentMethod = paymentMethod;
        }
    }
}
