package com.ecommerce.orders.module;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.ecommerce.orders.module.dto.CreateOrderDTO;
import com.ecommerce.orders.module.dto.OrderByIdDTO;

import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("orders")
@RequiredArgsConstructor
public class OrderController {
	
	private final OrderService orderService;

	@PostMapping("")
	public ResponseEntity<Void> createOrder(@RequestBody CreateOrderDTO dto) {
	    orderService.createOrder(dto);
	    return ResponseEntity.status(HttpStatus.CREATED).build();
	}

	@GetMapping("")
	public ResponseEntity<List<OrderByIdDTO>> getAllOrders() {
	    List<OrderByIdDTO> orders = orderService.getAllOrders();
	    return ResponseEntity.ok(orders);
	}

}
