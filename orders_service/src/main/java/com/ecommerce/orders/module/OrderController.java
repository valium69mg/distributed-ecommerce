package com.ecommerce.orders.module;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.http.HttpHeaders;
import com.ecommerce.orders.module.dto.CreateOrderDTO;
import com.ecommerce.orders.module.dto.OrderByIdDTO;

import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("orders")
@RequiredArgsConstructor
public class OrderController {
	
	private final OrderService orderService;

	@PostMapping("")
	public ResponseEntity<Void> createOrder(@RequestBody CreateOrderDTO dto, @RequestHeader(HttpHeaders.AUTHORIZATION) String token) {
	    orderService.createOrder(dto, token);
	    return ResponseEntity.status(HttpStatus.CREATED).build();
	}

	@GetMapping("")
	public ResponseEntity<List<OrderByIdDTO>> getAllOrders() {
	    List<OrderByIdDTO> orders = orderService.getAllOrders();
	    return ResponseEntity.ok(orders);
	}
	
	@GetMapping("{id}")
	public ResponseEntity<OrderByIdDTO> getAllOrders(@PathVariable Integer id) {
	    OrderByIdDTO order = orderService.getOrderById(id);
	    return ResponseEntity.ok(order);
	}

}
