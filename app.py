import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items, stores

app = Flask(__name__)

@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}

@app.post("/store")
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(
            400,
            message="Bad request. Ensure name is included in the JSON payload."
        )
    for store in stores.values():
        if store_data['name'] == store['name']:
            abort(400, message=f"store {store['name']} already exits")
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201

@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="store not found")

@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}

@app.post("/item")
def create_item():
    item_data = request.get_json()
    if(
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            message=" bad request, ensure price, store_id and name are included in the JSON payload"
        )
    for item in items.values():
        if (
            item_data['name'] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, message="item already exists")

    if item_data["store_id"] not in stores:
        abort(404, message="store not found")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] =item
    return item, 201 

@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="item not found")

@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    print(item_data)
    if "price" not in item_data or "name" not in item_data:
        abort(400, message="ensure all data is provided (price, name)")
    try:
        item = items[item_id]
        item |= item_data
        return item
    
    except KeyError:
        abort(404, message="item not found")

@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "item deleted"}
    except KeyError:
        abort(404, message="item not found")