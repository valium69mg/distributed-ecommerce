package com.ecommerce.orders.module;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

import com.ecommerce.orders.kafka.module.KafkaService;
import com.ecommerce.orders.kafka.module.dto.EventType;
import com.ecommerce.orders.kafka.module.dto.OrderEventDTO;
import com.ecommerce.orders.module.dto.CreateOrderDTO;
import com.ecommerce.orders.module.dto.OrderByIdDTO;
import com.ecommerce.orders.module.dto.OrderStatus;
import com.ecommerce.orders.module.entity.Order;
import com.ecommerce.orders.module.entity.OrderProduct;
import com.ecommerce.orders.module.repository.OrderProductRepository;
import com.ecommerce.orders.module.repository.OrderRepository;
import com.ecommerce.orders.products.module.ProductsService;
import com.ecommerce.orders.products.module.dto.ProductRead;

import jakarta.persistence.EntityNotFoundException;
import jakarta.persistence.criteria.CriteriaBuilder.Case;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@RequiredArgsConstructor
@Slf4j
public class OrderService {

	private final OrderRepository orderRepository;
	private final OrderProductRepository orderProductRepository;
	private final KafkaService kafkaService;
	private final ProductsService productsService;
	
	@Transactional
	public void createOrder(CreateOrderDTO dto, String token) {
		Order newOrder = new Order();
		newOrder.setUserId(dto.getUserId());
		newOrder.setCurrencyType(dto.getCurrencyType());
		newOrder.setStatus(OrderStatus.PENDING);
		
		List<Integer> productIds = dto.getProducts().stream().map(p -> p.getProductId()).toList();
		Map<Integer, Double> productPriceMap = productsService
		    .getProductsByIds(productIds, token)
		    .stream()
		    .collect(Collectors.toMap(
		        ProductRead::getId,     
		        ProductRead::getPrice   
		    ));
		
		List<OrderProduct> orderProducts =  dto.getProducts().stream().map(p -> {
			OrderProduct newOrderProduct = new OrderProduct();
			newOrderProduct.setOrder(newOrder);
			newOrderProduct.setPricePerUnit(productPriceMap.get(p.getProductId()));
			newOrderProduct.setUnits(p.getUnits());
			newOrderProduct.setProductId(p.getProductId());
			return newOrderProduct;
		}).toList();
		
		orderRepository.save(newOrder);
		orderProductRepository.saveAll(orderProducts);
		
		OrderEventDTO orderEventDTO = kafkaService.createOrderEventDTO(newOrder, orderProducts);
		kafkaService.sendOrderEvent(orderEventDTO);
		
	}
	
	public List<OrderByIdDTO> getAllOrders() {
		List<Order> orders = orderRepository.findAll();
		List<OrderByIdDTO> orderByIdDTOs =  orders.stream().map(o -> {
			OrderByIdDTO orderByIdDTO = new OrderByIdDTO();
			orderByIdDTO.setOrderId(o.getOrderId());
			orderByIdDTO.setUserId(o.getUserId());
		    orderByIdDTO.setStatus(o.getStatus());
			List<OrderProduct> orderProducts = orderProductRepository.findByOrder(o);
			double total = orderProducts.stream().mapToDouble(op -> op.getUnits() * op.getPricePerUnit()).sum();
			List<OrderByIdDTO.ProductByIdDTO> productByIdDTOs = orderProducts.stream().map(op -> {
				OrderByIdDTO.ProductByIdDTO productByIdDTO = new OrderByIdDTO.ProductByIdDTO();
				productByIdDTO.setPricePerUnit(op.getPricePerUnit());
				productByIdDTO.setUnits(op.getUnits());
				productByIdDTO.setProductId(op.getProductId());
				productByIdDTO.setTotalPrice(op.getUnits() * op.getPricePerUnit());
				return productByIdDTO;
			}).toList();
			orderByIdDTO.setTotal(total);
			orderByIdDTO.setProducts(productByIdDTOs);
			return orderByIdDTO;
		}).toList();
		return orderByIdDTOs;
	}
	
	public OrderByIdDTO getOrderById(int id) {
	    Optional<Order> optionalOrder = orderRepository.findById(id);
	    if (optionalOrder.isEmpty()) {
	        throw new EntityNotFoundException("Order with ID " + id + " not found");
	    }

	    Order order = optionalOrder.get();
	    OrderByIdDTO orderByIdDTO = new OrderByIdDTO();
	    orderByIdDTO.setOrderId(order.getOrderId());
	    orderByIdDTO.setUserId(order.getUserId());
	    orderByIdDTO.setStatus(order.getStatus());

	    List<OrderProduct> orderProducts = orderProductRepository.findByOrder(order);

	    double total = orderProducts.stream()
	        .mapToDouble(op -> op.getUnits() * op.getPricePerUnit())
	        .sum();

	    List<OrderByIdDTO.ProductByIdDTO> productByIdDTOs = orderProducts.stream()
	        .map(op -> {
	            OrderByIdDTO.ProductByIdDTO productByIdDTO = new OrderByIdDTO.ProductByIdDTO();
	            productByIdDTO.setPricePerUnit(op.getPricePerUnit());
	            productByIdDTO.setUnits(op.getUnits());
	            productByIdDTO.setProductId(op.getProductId());
	            productByIdDTO.setTotalPrice(op.getUnits() * op.getPricePerUnit());
	            return productByIdDTO;
	        })
	        .toList();

	    orderByIdDTO.setTotal(total);
	    orderByIdDTO.setProducts(productByIdDTOs);

	    return orderByIdDTO;
	}
	
	@KafkaListener(topics = "product-events", groupId = "order-consumer-group", containerFactory = "kafkaListenerContainerFactory")
    public void consumeOrderEvent(OrderEventDTO event) {
		switch (event.getType()) {
		case EventType.APPROVED_STOCK: {
			log.info("Received Kafka event: {}", event);
	        Optional<Order> orderOpt = orderRepository.findById(event.getOrderId());
	        if (orderOpt.isPresent()) {
	        	Order order = orderOpt.get();
	        	order.setStatus(OrderStatus.CONFIRMED);
	        	orderRepository.save(order);
	        } 
			break;
			
		}
		case EventType.NO_STOCK: {
			log.info("Received Kafka event: {}", event);
	        Optional<Order> orderOpt = orderRepository.findById(event.getOrderId());
	        if (orderOpt.isPresent()) {
	        	Order order = orderOpt.get();
	        	order.setStatus(OrderStatus.CANCELED);
	        	orderRepository.save(order);
	        } 
			break;
		}
		default:
			log.error("Unexpected value: " + event.getType());
		}
		
        
    }


	
}
