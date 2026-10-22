# Power BI Data Model Documentation

This document defines the roles, schemas, and relationships of the RetailIQ data model. This star-schema model is designed to facilitate robust enterprise analytics and seamless integration with downstream machine learning prediction facts.

## Table Roles

| Table Name | Role | Primary Key / Joins | Description |
| :--- | :--- | :--- | :--- |
| **`dim_customers`** | Dimension | `CustomerID` | Customer demographics, tenure, RFM metrics, and K-Means segment names. |
| **`dim_products`** | Dimension | `ProductID` | Product catalog containing product categories, subcategories, unit prices, and unit costs. |
| **`dim_stores`** | Dimension | `StoreID` | Retail store physical locations, cities, and regions. |
| **`fact_sales`** | Fact | `TransactionID` | Transactional sales orders including quantities, discounts, margins, and pre-registration flags. |
| **`fact_forecast`** | Fact | `Date` (Join to Calendar) | XGBoost test-set daily forecasting predictions vs. actual revenues. |
| **`fact_demand`** | Fact | `ProductID` | Product-level weekly unit sales predictions. |
| **`fact_model_summary`** | Fact | None (Standalone Reference) | Metrics and summary metadata for all three ML models. |
| **`Calendar`** | Dimension | `Date` | Continuous date lookup table generated via DAX. |

---

## Relationships Map

To build the relationship canvas in Power BI Desktop, establish the following links:

1. **`dim_customers[CustomerID]` &rarr; `fact_sales[CustomerID]`**
   - **Cardinality:** One-to-Many (`1:*`)
   - **Cross-Filter Direction:** Single (`dim_customers` filters `fact_sales`)
2. **`dim_products[ProductID]` &rarr; `fact_sales[ProductID]`**
   - **Cardinality:** One-to-Many (`1:*`)
   - **Cross-Filter Direction:** Single (`dim_products` filters `fact_sales`)
3. **`dim_stores[StoreID]` &rarr; `fact_sales[StoreID]`**
   - **Cardinality:** One-to-Many (`1:*`)
   - **Cross-Filter Direction:** Single (`dim_stores` filters `fact_sales`)
4. **`Calendar[Date]` &rarr; `fact_sales[Date]`**
   - **Cardinality:** One-to-Many (`1:*`)
   - **Cross-Filter Direction:** Single (`Calendar` filters `fact_sales`)
5. **`Calendar[Date]` &rarr; `fact_forecast[Date]`**
   - **Cardinality:** One-to-Many (`1:*`)
   - **Cross-Filter Direction:** Single (`Calendar` filters `fact_forecast`)
6. **`dim_products[ProductID]` &rarr; `fact_demand[ProductID]`**
   - **Cardinality:** One-to-Many (`1:*`)
   - **Cross-Filter Direction:** Both (Allows category slicing on demand predictions)

---

## ASCII Star Schema Diagram

```text
       +-------------------+             +-------------------+
       |   dim_customers   |             |   dim_products    |
       | ----------------- |             | ----------------- |
       |   CustomerID (PK) |             |   ProductID (PK)  |
       +---------+---------+             +---------+---------+
                 |                                 |
                 | 1                               | 1
                 |                                 |
                 | *                               | *
       +---------v---------------------------------v---------+
       |                    fact_sales                       |
       | --------------------------------------------------- |
       |  TransactionID (PK)                                 |
       |  CustomerID (FK)                                    |
       |  ProductID (FK)                                     |
       |  StoreID (FK)                                       |
       |  Date (FK)                                          |
       +---------^---------------------------------^---------+
                 |                                 |
                 | *                               | *
                 |                                 |
                 | 1                               | 1
       +---------+---------+             +---------+---------+
       |     Calendar      |             |    dim_stores     |
       | ----------------- |             | ----------------- |
       |     Date (PK)     |             |    StoreID (PK)   |
       +---------+---------+             +-------------------+
                 |
                 | 1
                 |
                 | *
       +---------v---------+
       |   fact_forecast   |
       | ----------------- |
       |     Date (FK)     |
       +-------------------+
```
