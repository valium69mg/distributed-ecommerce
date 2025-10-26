package com.ecommerce.orders.module.dto;

import java.util.List;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor

public class OrderByIdDTO {

	private Integer orderId;
	private String userId;
	private List<ProductByIdDTO> products;
	private Double total;
	private OrderStatus status;
	
	@Data
	@Builder
	@AllArgsConstructor
	@NoArgsConstructor
	public static class ProductByIdDTO {
		private Double pricePerUnit;
		private Integer units;
		private Integer productId;
		private Double totalPrice;
	}

}
