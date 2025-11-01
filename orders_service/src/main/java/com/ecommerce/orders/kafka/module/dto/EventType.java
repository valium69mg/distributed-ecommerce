package com.ecommerce.orders.kafka.module.dto;

import lombok.Getter;

@Getter
public enum OrderEventType {

	CREATE,
    APPROVED_STOCK,
    NO_STOCK,
	
}
