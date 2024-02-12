## Different Order Types

### Market Order
A market order is a request to buy or sell a security at the currently available market price. It provides the most likely method of filling an order. Market orders fill nearly instantaneously.

As a trade-off, your fill price may slip depending on the available liquidity at each price level as well as any price moves that may occur while your order is being routed to its execution venue. There is also the risk with market orders that they may get filled at unexpected prices due to short-term price spikes.

### Limit Order
A limit order is an order to buy or sell at a specified price or better. A buy limit order (a limit order to buy) is executed at the specified limit price or lower (i.e., better). Conversely, a sell limit order (a limit order to sell) is executed at the specified limit price or higher (better). Unlike a market order, you have to specify the limit price parameter when submitting your order.

While a limit order can prevent slippage, it may not be filled for a quite a bit of time, if at all. For a buy limit order, if the market price is within your specified limit price, you can expect the order to be filled. If the market price is equivalent to your limit price, your order may or may not be filled; if the order cannot immediately execute against resting liquidity, then it is deemed non-marketable and will only be filled once a marketable order interacts with it. You could miss a trading opportunity if price moves away from the limit price before your order can be filled.

### Stop Orders
A stop (market) order is an order to buy or sell a security when its price moves past a particular point, ensuring a higher probability of achieving a predetermined entry or exit price. Once the order is elected, the stop order becomes a market order. Alpaca converts buy stop orders into stop limit orders with a limit price that is 4% higher than a stop price < $50 (or 2.5% higher than a stop price >= $50). Sell stop orders are not converted into stop limit orders.

A stop order does not guarantee the order will be filled at a certain price after it is converted to a market order.

### Stop Limit Order
A stop-limit order is a conditional trade over a set time frame that combines the features of a stop order with those of a limit order and is used to mitigate risk. The stop-limit order will be executed at a specified limit price, or better, after a given stop price has been reached. Once the stop price is reached, the stop-limit order becomes a limit order to buy or sell at the limit price or better. In the case of a gap down in the market that causes the election of your order, but not the execution, you order will remain active as a limit order until it is executable or cancelled.

For this strategy, we are assuming that the new's is highly polarising, and that it will result in high momentum. As such, we want to enter into buy/sell position as soon as possible, and will place a **market order**.

If impact > 70 (**impact_buy**), it is an indication that the equity is bullish. Hence, we want to place a **buy order** with a **take profit** of **1%** (**tp**) and **stop loss** of **0.5%** (**sl**).
If impact < 30 (**impact_sell**), it is bearish, and we want to place a **sell order** with a **take profit** of **1%** and **stop loss** of **0.5%**.

The parameters we might want to tweak are the **impact_buy, impact_sell, tp and sl**.