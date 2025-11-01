package com.ecommerce.orders.kafka.module.dto;

import lombok.Getter;

@Getter
public enum EventType {

	CREATE,
    APPROVED_STOCK,
    NO_STOCK,
	
}
