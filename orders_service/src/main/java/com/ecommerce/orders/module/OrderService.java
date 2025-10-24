package com.ecommerce.orders.module;

import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Service;

import com.ecommerce.orders.module.dto.CreateOrderDTO;
import com.ecommerce.orders.module.dto.OrderByIdDTO;
import com.ecommerce.orders.module.entity.Order;
import com.ecommerce.orders.module.entity.OrderProduct;
import com.ecommerce.orders.module.repository.OrderProductRepository;
import com.ecommerce.orders.module.repository.OrderRepository;

import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class OrderService {

	private final OrderRepository orderRepository;
	private final OrderProductRepository orderProductRepository;
	
	@Transactional
	public void createOrder(CreateOrderDTO dto) {
		Order newOrder = new Order();
		newOrder.setUserId(dto.getUserId());
		newOrder.setCurrencyType(dto.getCurrencyType());
		
		
		List<OrderProduct> orderProducts =  dto.getProducts().stream().map(p -> {
			OrderProduct newOrderProduct = new OrderProduct();
			newOrderProduct.setOrder(newOrder);
			newOrderProduct.setPricePerUnit(p.getPricePerUnit());
			newOrderProduct.setUnits(p.getUnits());
			newOrderProduct.setProductId(p.getProductId());
			return newOrderProduct;
		}).toList();
		
		orderRepository.save(newOrder);
		orderProductRepository.saveAll(orderProducts);
		
	}
	
	public List<OrderByIdDTO> getAllOrders() {
		List<Order> orders = orderRepository.findAll();
		return orders.stream().map(o -> {
			OrderByIdDTO orderByIdDTO = new OrderByIdDTO();
			orderByIdDTO.setOrderId(o.getOrderId());
			orderByIdDTO.setUserId(o.getUserId());
			List<OrderProduct> orderProducts = orderProductRepository.findByOrder(o);
			List<OrderByIdDTO.ProductByIdDTO> productByIdDTOs = orderProducts.stream().map(op -> {
				OrderByIdDTO.ProductByIdDTO productByIdDTO = new OrderByIdDTO.ProductByIdDTO();
				productByIdDTO.setPricePerUnit(op.getPricePerUnit());
				productByIdDTO.setUnits(op.getUnits());
				productByIdDTO.setProductId(op.getProductId());
				return productByIdDTO;
			}).toList();
			orderByIdDTO.setProducts(productByIdDTOs);
			return orderByIdDTO;
		}).toList();
	}
	
}
