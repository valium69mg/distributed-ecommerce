package com.ecommerce.orders.module.dto;

import lombok.Getter;

@Getter
public enum OrderStatus {

	PENDING,
	PAYED,
	CONFIRMED,
	SHIPPED,
	DELIVERED,
	CANCELED
}
