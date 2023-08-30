from ast import Delete
from flask import request, Response, jsonify
from flask_restful import Resource
from DB_Handler import DBHandler
import json


class ConfigPharmacist(Resource):
    # Get specific pharmacist
    def get(self, userName):
        pharHnd = DBHandler()
        obj = pharHnd.getPharmacist(userName)
        if not obj:
            return
        return {'id': obj.pharmacist_id, 'name': obj.pharmacist_name, 'phone': obj.pharmacist_phoneNo,
                'userName': obj.pharmacist_userName, 'password': obj.pharmacist_password,
                'salary': obj.pharmacist_salary}, 200

    # Add new pharmacist
    def post(self, userName):
        obj = request.get_json()
        print(obj)
        pharHnd = DBHandler()
        id = pharHnd.addPharmacist(
            obj["name"], obj["phone"], obj["userName"], obj["password"], obj["salary"])
        return {'id': str(id)}, 200

    # delete a pharmacist
    def delete(self, userName):
        pharHnd = DBHandler()
        pharHnd.deletePharma(userName)
        return {'deleted_username': userName}, 200

    # Update existing pharmacist
    def put(self, userName):
        obj = request.get_json()
        pharHnd = DBHandler()
        pharHnd.changeName(obj["name"], userName)
        pharHnd.changePass(obj["password"], userName)
        pharHnd.changeSalary(obj["salary"], userName)
        pharHnd.changePhone(obj["phone"], userName)
        return {'Added Pharmacist with UserName: ': str(userName)}, 200

# ******************************************************************************************

# To get All Pharmacists


class Pharmacists(Resource):
    def get(self):
        pharHnd = DBHandler()
        obj = pharHnd.getAllPharmacists()
        if not obj:
            return
        json_object = json.dumps(obj, indent=4)
        return json_object, 200

# ******************************************************************************************


class Products(Resource):

    # to get all products
    def get(self):
        prodHnd = DBHandler()
        obj = prodHnd.getAllProducts()
        if not obj:
            return
        json_object = json.dumps(obj, indent=4)
        return json_object, 200

    # to add a new product
    def post(self):
        obj = request.get_json()
        prodHnd = DBHandler()
        prodHnd.addProduct(obj["name"], obj["price"],
                           obj["vendor"], obj["desc"])
        return {'Added Product': str(obj["name"])}, 200

# ******************************************************************************************


class Product(Resource):

    # this to add a new batch to existing product
    def post(self, id):
        prodHnd = DBHandler()
        obj = request.get_json()
        prodHnd.updateProduct(id, obj["quantity"], obj["batch_expiry"])
        return {'Added Batch to Product': str(id)}, 200

    # to delete a existinf product
    def delete(self, id):
        prodHnd = DBHandler()
        prodHnd.removeProductsFromOrderProd(id)
        prodHnd.removeProduct(id)
        return {'Deleted Product with ID': str(id)}, 200

    # to update a existing product
    def put(self, id):
        prodHnd = DBHandler()
        obj = request.get_json()
        prodHnd.changeName(id, obj["name"])
        prodHnd.changePPU(id, obj["price"])
        prodHnd.changeVendor(id, obj["vendor"])
        prodHnd.changeDesc(id, obj["desc"])
        return {'Chenged Product with id': str(id)}, 200


# ******************************************************************************************

class Batches(Resource):

    # Get all batches for all products
    def get(self):
        batchHnd = DBHandler()
        obj = batchHnd.getAllBatches()

        if not obj:
            return
        json_object = json.dumps(obj, indent=4)
        return json_object, 200

# ******************************************************************************************


class Batch(Resource):

    # delete a specific batch of specific product
    def delete(self, prodId, batchNo):
        print('*****', prodId, batchNo)
        batchHnd = DBHandler()
        flag = batchHnd.removeBatchByProductIdAndBatchNo(prodId, batchNo)
        if not flag:
            raise Exception('Batch was not deleted')
        return {'Deleted Batch # ': str(batchNo),
                'Product ID of that batch was': str(prodId)}, 200


# ******************************************************************************************


class ConfigureOrder(Resource):

    # take order and update data
    def post(self, name, price):
        dbHnd = DBHandler()
        obj = request.get_json()
        ord = dbHnd.addNewOrder(name)
        dbHnd.addTransactionRecord(price, ord)

        # prod = dbHnd.getProductById(prod[0])
        for prod in obj:
            p = dbHnd.getProductById(prod[0])
            dbHnd.removeProductQuantity(prod[0], int(prod[3]))
            dbHnd.addRecordForOrderProducts(prod[3], ord, p)

# ******************************************************************************************


class ProductsCloseToExpire(Resource):

    # Get all products that are within 60 days of expiry
    def get(self):
        batchHnd = DBHandler()
        obj = batchHnd.getAllProductsCloseToExpiry()
        if not obj:
            return
        json_object = json.dumps(obj, indent=4)
        return json_object, 200

# ******************************************************************************************


class ExpiredProducts(Resource):

    # Get all products that are expired
    def get(self):
        batchHnd = DBHandler()
        obj = batchHnd.getAllExpiredProducts()
        if not obj:
            return
        json_object = json.dumps(obj, indent=4)
        return json_object, 200


# ******************************************************************************************


class ProductsLowOnStock(Resource):

    # Get all products that are low on stock (<=500)
    def get(self):
        batchHnd = DBHandler()
        obj = batchHnd.getAllProductsLowOnQunatity()
        if not obj:
            return
        json_object = json.dumps(obj, indent=4)
        return json_object, 200
# ******************************************************************************************


class OrderRecsWithTransacDetail(Resource):

    # Get all Order records with their trsnsactionAmount
    def get(self):
        batchHnd = DBHandler()
        obj = batchHnd.getAllOrderRecs()
        if not obj:
            return
        json_object = json.dumps(obj, indent=4)
        return json_object, 200

# ******************************************************************************************


class OrderProductRecs(Resource):

    # Get all OrderedProducts of all the orders
    def get(self):
        batchHnd = DBHandler()
        print('JJJJJJJJJJJJJJJJJJ')
        obj = batchHnd.getALLOrderProdsRecs()
        if not obj:
            return
        json_object = json.dumps(obj, indent=4)
        return json_object, 200

# ******************************************************************************************


def initialize_routes(api):
    api.add_resource(ConfigPharmacist, '/api/pharmacist/<userName>')
    api.add_resource(Pharmacists, '/api/pharmacists')
    api.add_resource(Products, '/api/products')
    api.add_resource(Batches, '/api/batches')

    api.add_resource(Batch, '/api/batch/<prodId>/<batchNo>')

    api.add_resource(Product, '/api/product/<id>')
    api.add_resource(ConfigureOrder, '/api/completeOrder/<name>/<price>')

    api.add_resource(ProductsCloseToExpire, '/api/productsCloseToExpire')
    api.add_resource(ExpiredProducts, '/api/expiredProducts')
    api.add_resource(ProductsLowOnStock, '/api/productsLowOnStock')

    api.add_resource(OrderRecsWithTransacDetail,
                     '/api/orderRecsWithTransacDetail')
    api.add_resource(OrderProductRecs, '/api/orderProductRecs')
