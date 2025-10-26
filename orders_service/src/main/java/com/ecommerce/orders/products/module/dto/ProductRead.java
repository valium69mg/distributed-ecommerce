package com.ecommerce.orders.products.module.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class ProductRead {
    private int id;
    private String name;
    private String description;
    private double price;
    private int stock;
    private String user_id;
}
