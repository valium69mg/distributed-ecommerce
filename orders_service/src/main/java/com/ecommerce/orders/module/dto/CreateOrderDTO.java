package com.ecommerce.orders.module.dto;


import java.util.List;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class CreateOrderDTO {

	private String userId;
	private CurrencyType currencyType;
	private List<ProductForOrderDTO> products;

	@Data
	@Builder
	@AllArgsConstructor
	@NoArgsConstructor
	public static class ProductForOrderDTO {
		private Integer units;
		private Integer productId;
	}

}
