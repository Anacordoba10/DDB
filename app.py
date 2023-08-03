#Ana Cordoba V-C.I: 29.655.207
from flask import Flask, request, jsonify
import uuid
from datetime import datetime

app = Flask(__name__)

customers_data = []
orders_data = []

#Crear cliente
@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.json

    if not data:
        return jsonify({"error": "Los datos del cliente no fueron proporcionados."}), 400

    required_fields = ['nombre', 'cedula', 'whatsapp', 'email']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"error": f"Los siguientes campos son requeridos: {', '.join(missing_fields)}"}), 400

    customers_data.append(data)

    return jsonify({"message": "Cliente creado exitosamente.", "data": data}), 201

#Editar cliente
@app.route('/customers/<cedula>', methods=['PUT'])
def update_customer(cedula):
    data = request.json

    if not data:
        return jsonify({"error": "Los datos del cliente no fueron proporcionados."}), 400

    customer_to_update = next((customer for customer in customers_data if customer["cedula"] == cedula), None)

    if not customer_to_update:
        return jsonify({"error": "Cliente no encontrado."}), 404

    data.pop("cedula", None)

    customer_to_update.update(data)

    return jsonify({"message": "Cliente actualizado exitosamente.", "data": customer_to_update}), 200

#Lista de cliente
@app.route('/customers', methods=['GET'])
def list_customers():
    return jsonify({"data": customers_data}), 200

#Crear pedido
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json

    if not data:
        return jsonify({"error": "Los datos del pedido no fueron proporcionados."}), 400

    required_fields = ['numero_identificador', 'cantidad_hamburguesas', 'monto_delivery', 'total_pagar',
                       'modo_pago', 'screenshot_pago', 'status', 'fecha_hora', 'direccion_delivery',
                       'cedula-cliente', 'observaciones']

    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"error": f"Los siguientes campos son requeridos: {', '.join(missing_fields)}"}), 400

    order = {
        "numero_identificador": data["numero_identificador"],
        "cantidad_hamburguesas": data["cantidad_hamburguesas"],
        "monto_delivery": data["monto_delivery"],
        "total_pagar": data["total_pagar"],
        "modo_pago": data["modo_pago"],
        "screenshot_pago": None,
        "status": data["status"],
        "fecha_hora": data["fecha_hora"],
        "direccion_delivery": data["direccion_delivery"],
        "cedula-cliente": data["cliente"]["cedula"] ,
        "observaciones": data["observaciones"]
    }

    orders_data.append(order)

    return jsonify({"message": "Pedido creado exitosamente.", "data": order}), 201

#Actualizar status del pedido
@app.route('/orders/<int:id>/status', methods=['PATCH'])
def update_order_status(id):
    data = request.json

    if not data:
        return jsonify({"error": "Los datos de actualización del estado no fueron proporcionados."}), 400

    order_to_update = next((order for order in orders_data if order["numero_identificador"] == id), None)

    if not order_to_update:
        return jsonify({"error": "Pedido no encontrado."}), 404

    order_to_update["status"] = data.get("status", order_to_update["status"])

    return jsonify({"message": "Estado del pedido actualizado exitosamente.", "data": order_to_update}), 200

#Proporcionar Screenshot
@app.route('/orders/<int:id>/payment-screenshot', methods=['POST'])
def upload_payment_screenshot(id):

    if 'screenshot' not in request.files:
        return jsonify({"error": "No se proporcionó ningún archivo de screenshot."}), 400

    screenshot_file = request.files['screenshot']

    if screenshot_file.filename == '' or not (screenshot_file.filename.lower().endswith(('.jpg', '.jpeg', '.png'))):
        return jsonify({"error": "Se debe proporcionar un archivo válido en formato jpg o png."}), 400

    order = next((order for order in orders_data if order["numero_identificador"] == id), None)

    if not order:
        return jsonify({"error": "Pedido no encontrado."}), 404

    order["screenshot_pago"] = screenshot_file.filename

    return jsonify({"message": "Screenshot del pago enviado exitosamente.", "data": order}), 200

#lista de ordenes
@app.route('/orders', methods=['GET'])
def list_orders():
    date = request.args.get('date')
    status = request.args.get('status')
    cedula = request.args.get('cedula')

    filtered_orders = orders_data

    if date:
        filtered_orders = [order for order in filtered_orders if order["fecha_hora"].startswith(date)]

    if status:
        filtered_orders = [order for order in filtered_orders if order["status"].lower() == status.lower()]

    if cedula:
        filtered_orders = [order for order in filtered_orders if order["cliente"]["cedula"] == cedula]

    output_list = []
    for order in filtered_orders:
        output_order = {
            "quantity": order["cantidad_hamburguesas"],
            "payment_method": order["modo_pago"],
            "remarks": order["observaciones"],
            "direccion_delivery": order["municipio"]["ciudad"],
            "cedula": order["cliente"]["cedula"],
            "total": order["total_pagar"],
            "payment_screenshot": order["screenshot_pago"],
            "status": order["status"],
            "delivery_amount": order["monto_delivery"],
            "order_number": order["numero_identificador"],
            "datetime": order["fecha_hora"]
        }
        output_list.append(output_order)

    return jsonify(output_list), 200

if __name__ == '__main__':
    app.run(debug=True)
