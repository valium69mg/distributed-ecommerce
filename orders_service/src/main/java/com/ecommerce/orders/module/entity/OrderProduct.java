package com.ecommerce.orders.module.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Data
@AllArgsConstructor
@NoArgsConstructor
@Table(name = "order_products")
public class OrderProduct {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name = "order_product_id")
	private Integer orderProductId;
	
	@Column(name = "product_id")
	private Integer productId;
	
	@Column(name = "units")
	private Integer units;
	
	@Column(name = "price_per_unit")
	private Double pricePerUnit;
	
	@ManyToOne
	@JoinColumn(name = "order_id")
	private Order order;
	
}
