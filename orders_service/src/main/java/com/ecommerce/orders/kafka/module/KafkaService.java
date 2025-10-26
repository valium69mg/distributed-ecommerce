package com.ecommerce.orders.kafka.module;

import java.util.List;

import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

import com.ecommerce.orders.kafka.module.dto.OrderEventDTO;
import com.ecommerce.orders.kafka.module.dto.OrderEventType;
import com.ecommerce.orders.kafka.module.dto.OrderEventDTO.ProductEventDTO;
import com.ecommerce.orders.module.entity.Order;
import com.ecommerce.orders.module.entity.OrderProduct;
import com.fasterxml.jackson.databind.ObjectMapper;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Slf4j
public class KafkaService {

	private final KafkaTemplate<String, String> kafkaTemplate;
	private final ObjectMapper objectMapper;

	public OrderEventDTO createOrderEventDTO(Order order, List<OrderProduct> orderProducts) {
		OrderEventDTO orderEventDTO = new OrderEventDTO();
		orderEventDTO.setOrderId(order.getOrderId());
		orderEventDTO.setType(OrderEventType.CREATE);
		List<ProductEventDTO> productEventDTOs = orderProducts.stream().map(op -> {
			ProductEventDTO productEventDTO = new ProductEventDTO();
			productEventDTO.setProductId(op.getProductId());
			productEventDTO.setUnits(op.getUnits());
			return productEventDTO;
		}).toList();
		orderEventDTO.setProducts(productEventDTOs);
		return orderEventDTO;
	}
	
	public void sendOrderEvent(OrderEventDTO dto) {
	    try {
	        String json = objectMapper.writeValueAsString(dto);
	        kafkaTemplate.send("order-events", json).get();
	        log.info("Kafka event sent: {}", json);
	    } catch (Exception e) {
	       log.error("Error sending event: {}", e.getMessage());
	    }
	}
	
}
