package com.ecommerce.orders.module.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.ecommerce.orders.module.entity.Order;
import com.ecommerce.orders.module.entity.OrderProduct;

public interface OrderProductRepository extends JpaRepository<OrderProduct, Integer>{

	List<OrderProduct> findByOrder(Order order);
}
