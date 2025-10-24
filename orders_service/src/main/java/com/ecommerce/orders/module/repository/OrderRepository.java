package com.ecommerce.orders.module.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.ecommerce.orders.module.entity.Order;

public interface OrderRepository extends JpaRepository<Order, Integer> {

}
