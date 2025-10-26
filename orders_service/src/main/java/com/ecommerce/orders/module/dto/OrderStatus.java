package com.ecommerce.orders.module.dto;

import lombok.Getter;

@Getter
public enum OrderStatus {

	PENDING,
	CONFIRMED,
	PAYED,
	SHIPPED,
	DELIVERED,
	CANCELED
}
