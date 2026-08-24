# Data Dictionary

## city_market_metrics.csv
| Field | Definition | Type | Unit | Source | Real/Synthetic |
|---|---|---|---|---|---|
| city | City Name | String | - | - | Real |
| state | State Name | String | - | - | Real |
| population | Total population estimate | Integer | Persons | Census | Real |
| households | Total households | Integer | Households | Census | Real |
| population_density | Persons per sq km | Integer | Persons/sq km | Census | Real |
| urbanization | Urbanization rate | Float | % | Census | Real |
| mpce | Monthly per capita expenditure | Integer | INR | MoSPI | Real |
| internet_penetration | Internet users | Float | % | OGD | Real |
| economic_growth | GDP growth proxy | Float | % | RBI | Real |
| income_proxy | Income level proxy | Integer | INR | RBI | Real |
| ecommerce_adoption | E-commerce usage | Float | % | Derived | Assumption |

## competitor_metrics.csv
| Field | Definition | Type | Unit | Source | Real/Synthetic |
|---|---|---|---|---|---|
| city | City Name | String | - | - | Real |
| competitor | Competitor Name | String | - | - | Real |
| presence | Is present? | Boolean | - | Public | Real |
| delivery_time | Avg delivery promise | Integer | Mins | Public | Real |
| category_count | Number of categories | Integer | Count | Public | Real |
| reported_users | Est. users | Integer | Users | Filings | Real |
| reported_aov | Est. AOV | Integer | INR | Filings | Real |
| reported_city_count | Total cities active | Integer | Count | Filings | Real |
| source | Data source | String | - | - | Real |
| source_date | Date of observation | Date | - | - | Real |
