### Deployed Server: https://platinumrx-assignment.onrender.com
###### (Note: There might be slight delays in the initial response because server cold starts when inactive but once a request is made then it'll be quick enough)


#### Endpoints:

**Request Type:** POST <br>
**URL:** https://platinumrx-assignment.onrender.com/transactions/initiate <br>
**Request Payload:** <br>
```json
{
    "order_id": "ORD134",
    "amount": 8299.0,
    "payment_instrument": {
        "type": "card",
        "card_number": "****",
        "expiry": "02/26"
    }
}
```

**Request Type:** POST <br>
**URL:** https://platinumrx-assignment.onrender.com/transactions/callback <br>
**Request Payload:** <br>
```json
{
  "order_id": "ORD134",
  "status": "failure",
  "gateway": "razorpay",
  "reason": "Customer Cancelled" // optional
}
```

Following endpoints are for checking the application's state and how Database is changing based on the above endpoints.
**Request Type:** GET <br>
**URL:** https://platinumrx-assignment.onrender.com/transactions-list <br>

**Request Type:** GET <br>
**URL:** https://platinumrx-assignment.onrender.com/gateways-list <br>


#### To add a new payment gateway:
1. Create a class inside `payment_gateways/gateway_clients`. Please make sure to follow the same pattern as other files in the other folder.
2. Add its constants for API Key (dummy) and weightage inside the `constants.py`.
3. Register this new gateway inside `payment_gateways/payment_gateway_manager.py` inside `initialize_gateways` function
