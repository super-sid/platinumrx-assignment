from flask import Blueprint, Flask, request, url_for

from payment_gateways.payment_gateway_manager import PaymentGatewayManager
from transactions.transactions_manager import TransactionsManager

app = Flask(__name__)

transactions_bp = Blueprint("transactions", __name__, url_prefix="/transactions")

payment_gateway_manager_obj = PaymentGatewayManager()
transactions_obj = TransactionsManager()
payment_gateway_manager_obj.initialize_gateways()


def null_checks_for_initiate(data):
    base_message = " missing from the request body"
    fields = ["order_id", "payment_instrument", "amount"]
    for field in fields:
        if data.get(field) is None:
            return True, field + base_message
    return False, ""


def null_checks_for_callback(data):
    base_message = " missing from the request body"
    fields = ["order_id", "status", "gateway"]
    for field in fields:
        if data.get(field) is None:
            return True, field + base_message
    return False, ""


@transactions_bp.route("/initiate", methods=["POST"])
def initiate():
    data = request.get_json()
    check, message = null_checks_for_initiate(data)
    if check:
        return message, 422
    order_id = data.get("order_id")
    chosen_gateway = payment_gateway_manager_obj.choose_gateway()
    if chosen_gateway is None:
        return "None of the Payment Gateways are available right now", 400
    transactions_obj.add(data)
    transactions_obj.add_payment_gateway_info(order_id, chosen_gateway.name)
    gateway_link = chosen_gateway.initiate_transaction(data)
    curr_transaction = transactions_obj.get_record(order_id)
    return {
        "message": "Transaction Created",
        "transaction": vars(curr_transaction),
        "gateway": chosen_gateway.name,
        "gateway_payment_link": gateway_link,
    }


@transactions_bp.route("/callback", methods=["POST"])
def callback():
    data = request.get_json()
    check, message = null_checks_for_callback(data)
    if check:
        return message, 422
    order_id = data.get("order_id")
    order_status = data.get("status")
    payment_gateway = data.get("gateway")
    transactions_obj.update_status(order_id, order_status, data.get("reason", ""))
    curr_transaction = transactions_obj.get_record(order_id)
    if payment_gateway not in ["razorpay", "payu", "stripe"]:
        return "Please provide a valid payment gateway", 422
    payment_gateway_manager_obj.update_gateway_on_status(payment_gateway, order_status)

    return {"message": "Transaction Updated", "transaction": vars(curr_transaction)}


@app.route("/transactions-list")
def get_transactions_list():
    records = transactions_obj._records
    output = []
    for _, record in records.items():
        output.append(vars(record))

    return output


@app.route("/gateways-list")
def get_payment_gateways_info():
    records = payment_gateway_manager_obj._gateways
    output = []
    for _, record in records.items():
        output.append(vars(record))
    return output


app.register_blueprint(transactions_bp)
