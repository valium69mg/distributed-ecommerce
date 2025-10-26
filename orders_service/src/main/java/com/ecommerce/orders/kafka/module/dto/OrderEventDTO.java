package com.ecommerce.orders.kafka.module.dto;

import java.util.List;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class OrderEventDTO {

	private Integer orderId;
	private OrderEventType type;
	private List<ProductEventDTO> products;
	
	@Data
	@AllArgsConstructor
	@NoArgsConstructor
	public static class ProductEventDTO {
		
		private Integer units;
		private Integer productId;
		
	}
}
