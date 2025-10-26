package com.ecommerce.orders.products.module;

import java.util.List;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import com.ecommerce.orders.products.module.dto.ProductRead;

import jakarta.annotation.PostConstruct;

@Service
public class ProductsService {

    @Value("${PRODUCTS_HOST}")
    private String productsHost;

    @Value("${PRODUCTS_PORT}")
    private String productsPort;

    private final WebClient.Builder builder;
    private WebClient webClient;

    public ProductsService(WebClient.Builder builder) {
        this.builder = builder;
    }

    @PostConstruct
    public void init() {
        String baseUrl = "http://" + productsHost + ":" + productsPort;
        this.webClient = builder.baseUrl(baseUrl).build();
    }

    public List<ProductRead> getProductsByIds(List<Integer> ids, String token) {
        return webClient.post()
            .uri("/products/")
            .header("Authorization", token)
            .bodyValue(ids)
            .retrieve()
            .bodyToFlux(ProductRead.class)
            .collectList()
            .block();
    }
}


