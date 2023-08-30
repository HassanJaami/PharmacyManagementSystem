
from DB_Base import startSession
from DB_Admin import Admin
from DB_Batch import Batch
from DB_Pharmacist import Pharmacist
from DB_Product import Product
from DB_Orders import Orders
from DB_OrderProduct import OrderProduct
from DB_TransactionDetail import TransactionDetail
from datetime import date, datetime, timedelta
import json


class DBHandler():
    def __init__(self):
        self.session = startSession()

    def __del__(self):
        self.session.close()

# *********************************************************************************************


# Admin


    def addAdmin(self, name, userName, password):
        obj = Admin(name, userName, password)
        self.session.add(obj)
        self.session.commit()

    def getAdmin(self, userName):
        obj = self.session.query(Admin).filter_by(
            admin_userName=userName).first()

        return obj

    def getAdminPass(self, userName):
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        obj = self.getAdmin(userName)
        print('#####################', obj.admin_userName)
        if not obj:
            return None
        return obj.admin_password

    def changeAdminName(self, name, userName):
        obj = self.getAdmin(userName)
        if not obj:
            return None
        obj.admin_name = name
        self.session.add(obj)
        self.session.commit()

    def changeAdminPass(self, pswd, userName):
        obj = self.getAdmin(userName)
        if not obj:
            return None
        obj.admin_password = pswd
        self.session.add(obj)
        self.session.commit()

    def deleteAdmin(self, userName):
        obj = self.getAdmin(userName)
        if not obj:
            return None
        self.session.delete(obj)
        self.session.commit()
# **********************************************************************************
# Batch

    def isBacth(self, productID):
        if (self.session.query(Batch).filter_by(product_id=productID).first()):
            return True
        else:
            return False

    def addBatch(self, batchNo, batchQuant, batchExp, p):
        obj = Batch(batchNo, batchQuant, batchExp, p)
        self.session.add(obj)
        self.session.commit()

    def updateBatch(self, prod, batchQuant, batchExpiry):
        print(batchExpiry)
        print(batchQuant)
        bNo = self.getLatestBatch(prod.product_id)
        print(bNo)

        if (bNo):
            batch_no = bNo + 1
            batch_quantity = batchQuant
            batch_expiry = batchExpiry
            self.addBatch(batch_no, batch_quantity, batch_expiry, prod)
            print(batch_no)
            print(batch_quantity)
            print(batch_expiry)
        elif (bNo == None):
            batch_no = 1
            batch_quantity = batchQuant
            batch_expiry = batchExpiry
            self.addBatch(batch_no, batch_quantity, batch_expiry, prod)
            print(batch_no)
            print(batch_quantity)
            print(batch_expiry)

    def removeAllBatch(self, prod):
        print(prod)
        obj = self.session.query(Batch).filter_by(
            product_id=prod.product_id).all()
        if (obj):
            for bat in obj:
                self.session.delete(bat)
                self.session.commit()
            return True
        else:
            return None

    def getLatestBatch(self, prodId):
        obj = self.session.query(Batch).filter_by(product_id=prodId).all()
        if (obj):
            for bt in obj:
                latestbNo = bt.batch_no
            return latestbNo
        else:
            print('Batch Does Not Exist')
            return None

        # to be converted in JSON later
    def getAllBatches(self):
        obj = self.session.query(Batch).all()
        if not obj:
            return None
        lis = []
        for batch in obj:
            dicObj = {}
            dicObj["product_id"] = batch.prod.product_id
            dicObj["batch_no"] = batch.batch_no
            dicObj["batch_quantity"] = batch.batch_quantity
            dicObj["batch_expiry"] = str(batch.batch_expiry)
            lis.append(dicObj)
        return lis

    def getTotalProductQuantity(self, prodId):
        obj = self.session.query(Batch).filter_by(product_id=prodId).all()
        res = 0
        for rec in obj:
            if rec.batch_expiry > date.today():
                res = res + rec.batch_quantity
        return res

# ******************************************************************************************
# Pharmacist

    def addPharmacist(self, name, phone, userName, password, salary):
        obj = Pharmacist(name, phone, userName, password, salary)
        self.session.add(obj)
        self.session.commit()
        return obj.pharmacist_userName

    def getPharmacist(self, userName):
        obj = self.session.query(Pharmacist).filter_by(
            pharmacist_userName=userName).first()
        return obj

    def getPharmPass(self, userName):
        obj = self.getPharmacist(userName)
        if not obj:
            return None
        return obj.pharmacist_password

    def changePharmName(self, name, userName):
        obj = self.getPharmacist(userName)
        if not obj:
            return None
        obj.pharmacist_name = name
        self.session.add(obj)
        self.session.commit()

    def changePharmPass(self, pswd, userName):
        obj = self.getPharmacist(userName)
        if not obj:
            return None
        obj.pharmacist_password = pswd
        self.session.add(obj)
        self.session.commit()

    def deletePharma(self, userName):
        obj = self.getPharmacist(userName)
        if not obj:
            return None
        self.session.delete(obj)
        self.session.commit()

    def changePharmSalary(self, salary, userName):
        obj = self.getPharmacist(userName)
        if not obj:
            return None
        obj.pharmacist_salary = salary
        self.session.add(obj)
        self.session.commit()

    def changePharmPhone(self, phone, userName):
        obj = self.getPharmacist(userName)
        if not obj:
            return None
        obj.pharmacist_phoneNo = phone
        self.session.add(obj)
        self.session.commit()

    # to be converted in JSON later
    def getAllPharmacists(self):
        obj = self.session.query(Pharmacist).all()
        if not obj:
            return None
        pharmacistDict = {}
        lis = []
        dicObj = {}
        for phar in obj:
            dicObj = {}
            dicObj["pharmacist_name"] = phar.pharmacist_name
            dicObj["pharmacist_phoneNo"] = phar.pharmacist_phoneNo
            dicObj["pharmacist_userName"] = phar.pharmacist_userName
            dicObj["pharmacist_password"] = phar.pharmacist_password
            dicObj["pharmacist_salary"] = phar.pharmacist_salary
            lis.append(dicObj)
        return lis

    def updateBatchQuantity(self, prod, batchNo, quant):
        print(batchNo)
        print(prod.product_id)
        obj = self.session.query(Batch).filter_by(
            product_id=prod.product_id, batch_no=batchNo).first()
        print(obj)
        obj.batch_quantity = quant
        print(obj.batch_quantity)
        self.session.add(obj)
        self.session.commit()

    def updateQuantity(self, prod, quantity):
        obj = self.session.query(Batch).filter_by(
            product_id=prod.product_id).all()
        print(quantity)
        if (obj):
            totalQuanttity = 0
            for bt in obj:
                totalQuanttity = totalQuanttity + bt.batch_quantity

        if (obj):
            if (totalQuanttity >= quantity):
                print('Request Can Be Fulfilled')
            else:
                print('Request Can Not Be Fulfilled!!')
                return None

            for bt in obj:
                if quantity > 0:
                    if (bt.batch_quantity <= quantity):
                        quantity = quantity - bt.batch_quantity
                        bt.batch_quantity = 0
                        print(bt.batch_quantity)
                        self.removeBatch(prod, bt.batch_no)
                    elif (bt.batch_quantity > quantity):
                        bt.batch_quantity = bt.batch_quantity - quantity
                        quantity = 0
                        print(bt.batch_quantity)
                        self.updateBatchQuantity(
                            prod, bt.batch_no, bt.batch_quantity)
        else:
            print('No Batch Found')

# *********************************************************************************************
# Product

    def getProduct(self, productName):
        obj = self.session.query(Product).filter_by(
            product_name=productName).first()
        if (obj):
            return obj
        else:
            return None

    def getProductId(self, productName):
        obj = self.session.query(Product).filter_by(
            product_name=productName).first()
        return obj.product_id

    def getProductById(self, prodId):
        obj = self.session.query(Product).filter_by(product_id=prodId).first()
        if (obj):
            return obj
        else:
            return None

    def addProduct(self, name, ppu, vendor, descip):
        obj = Product(name, ppu, vendor, descip)
        self.session.add(obj)
        self.session.commit()

    def changeName(self, id, newName):
        obj = self.getProductById(id)
        obj.product_name = newName
        self.session.add(obj)
        self.session.commit()

    def changeDesc(self, id, newDesc):
        obj = self.getProductById(id)
        obj.product_description = newDesc
        self.session.add(obj)
        self.session.commit()

    def changePPU(self, id, newPPU):
        obj = self.getProductById(id)
        obj.product_PPU = newPPU
        self.session.add(obj)
        self.session.commit()

    def changeVendor(self, id, newVendor):
        obj = self.getProductById(id)
        obj.product_vendor = newVendor
        self.session.add(obj)
        self.session.commit()

    def updateProduct(self, productID, prodQuant, prodExpiry):
        prod = self.getProductById(productID)
        if (prod == None):
            print('Product Does Not Exist')
        else:
            print('Exist!!')
            print(date.today())
            # if(prodExpiry <= date.today()):
            print('Enter date Greater than system date')
            # else:
            print(prod)
            # bat = BatchDBHndler()
            self.updateBatch(prod, prodQuant, prodExpiry)
            # bat.__del__()

    def removeProduct(self, prodId):
        prod = self.getProductById(prodId)
        if (prod == None):
            print('Product Does Not Exist')
        else:
            print('Exist!!')
            print(prod)
            # bat = BatchDBHndler()
            self.removeAllBatch(prod)
            # bat.__del__()
            deleProd = self.session.query(
                Product).filter_by(product_id=prodId).first()
            self.session.delete(deleProd)
            self.session.commit()

    def removeBatch(self, prod, batchNo):
        obj = self.session.query(Batch).filter_by(
            product_id=prod.product_id).all()
        if (obj):
            for bat in obj:
                if bat.batch_no == batchNo:
                    self.session.delete(bat)
                    self.session.commit()
                    return True
        return False

    def removeBatchByProductIdAndBatchNo(self, prodId, batchNo):
        obj = self.session.query(Batch).filter_by(product_id=prodId).all()
        print('all batches: ', obj[0].product_id)
        for batch in obj:
            print(batchNo, ' ??????? ', batch.batch_no)
            if int(batch.batch_no) == int(batchNo):
                print('lllllllll')
                self.session.delete(batch)
                self.session.commit()
                return True
        return False

    def removeProductBatch(self, prodId):
        prod = self.getProductById(prodId)
        if prod == None:
            print('Product Does Not Exist')
        else:
            print("Exist")
            print(prod)
            # bat = BatchDBHndler()
            self.removeBatch(prod)
            # bat.__del__()

    # to be converted in JSON later
    def getAllProducts(self):
        obj = self.session.query(Product).all()
        if not obj:
            return None
        lis = []
        dicObj = {}
        for prod in obj:
            dicObj = {}
            dicObj["product_id"] = prod.product_id
            dicObj["product_name"] = prod.product_name
            dicObj["product_PPU"] = prod.product_PPU
            dicObj["product_vendor"] = prod.product_vendor
            dicObj["product_description"] = prod.product_description
            dicObj["product_quantity"] = self.getTotalProductQuantity(
                prod.product_id)
            lis.append(dicObj)
        return lis

    def removeProductQuantity(self, prodId, quant):
        prod = self.getProductById(prodId)
        if prod == None:
            print('Product Does Not Exist')
        else:
            print(prod)
            obj = self.updateQuantity(prod, quant)

    def getAllProductsCloseToExpiry(self):
        # obj = self.session.query(Batch).filter_by(batch_no=4).first()
        # print('original ', obj.batch_expiry)

        # print('modie ', obj.batch_expiry-timedelta(days=60))
        # print('today ', date.today())

        # if obj.batch_expiry-timedelta(days=60) < date.today():
        #     print('ok ', obj.batch_expiry-timedelta(days=60) - date.today())

        lis = self.session.query(Batch).all()
        res = []
        for obj in lis:
            if obj.batch_expiry > date.today() and obj.batch_expiry-timedelta(days=60) <= date.today():
                dicObj = {}
                dicObj["product_id"] = obj.prod.product_id
                dicObj["product_name"] = obj.prod.product_name
                dicObj["batch_no"] = obj.batch_no
                dicObj["batch_quantity"] = obj.batch_quantity
                dicObj["batch_expiry"] = str(obj.batch_expiry)
                res.append(dicObj)
        return res

    def getAllExpiredProducts(self):
        lis = self.session.query(Batch).all()
        res = []
        for obj in lis:
            if obj.batch_expiry <= date.today():
                dicObj = {}
                dicObj["product_id"] = obj.prod.product_id
                dicObj["product_name"] = obj.prod.product_name
                dicObj["batch_no"] = obj.batch_no
                dicObj["batch_quantity"] = obj.batch_quantity
                dicObj["batch_expiry"] = str(obj.batch_expiry)
                res.append(dicObj)
        return res

    def getAllProductsLowOnQunatity(self):
        lis = self.session.query(Product).all()
        quant = 0
        res = []
        for prod in lis:
            quant = self.getTotalProductQuantity(prod.product_id)
            if quant <= 500:
                dicObj = {}
                dicObj["product_id"] = prod.product_id
                dicObj["product_name"] = prod.product_name
                dicObj["product_PPU"] = prod.product_PPU
                dicObj["product_vendor"] = prod.product_vendor
                dicObj["product_description"] = prod.product_description
                dicObj["product_quantity"] = quant
                res.append(dicObj)
        return res

    # ************************************************************************************************

# OrderProd

    def addRecordForOrderProducts(self, quantity, order, prod):
        obj = OrderProduct(quantity, order, prod)
        self.session.add(obj)
        self.session.commit()
        return obj

    def getALLOrderProdsRecs(self):
        obj = self.session.query(OrderProduct).all()
        res = []
        for ord in obj:
            dicObj = {}
            dicObj["order_id"] = ord.order_id
            dicObj["product_id"] = ord.product_id
            dicObj["product_name"] = ord.prod.product_name
            dicObj["orderProd_qty"] = ord.orderProd_qty
            res.append(dicObj)
        return res

    def removeProductsFromOrderProd(self, prodId):
        obj = self.session.query(OrderProduct).filter_by(
            product_id=prodId).all()

        for p in obj:
            self.session.delete(p)
            self.session.commit()


# Trsansaction:


    def addTransactionRecord(self, amount, order):
        obj = TransactionDetail(amount, order)
        self.session.add(obj)
        self.session.commit()
        return obj

    # def getAllTransactionRecs(self):
    #     pass

    def getTrsansacRecordByOrderId(self, ordId):
        obj = self.session.query(TransactionDetail).filter_by(
            order_id=ordId).first()
        if (obj):
            return obj.transac_amount
        else:
            return None

# Order

    def addNewOrder(self, name):
        obj = Orders(name)
        self.session.add(obj)
        self.session.commit()
        return obj

    def getOrderById(self, id):
        obj = self.session.query(Orders).filter_by(order_id=id).first()
        if (obj):
            return obj
        else:
            return None

    def getAllOrderRecs(self):
        obj = self.session.query(Orders).all()
        res = []
        for ord in obj:
            amount = self.getTrsansacRecordByOrderId(ord.order_id)
            dicObj = {}
            dicObj["order_id"] = ord.order_id
            dicObj["order_date"] = str(ord.order_date)
            dicObj["order_amount"] = amount
            dicObj["customer_name"] = ord.customer_name
            res.append(dicObj)
        return res


# hnd = DBHandler()
# p = hnd.getAllProductsCloseToExpiry()
# p = hnd.getAllExpiredProducts()
# p = hnd.getAllProductsLowOnQunatity()

# p = hnd.getAllOrderRecs()

# p = hnd.getALLOrderProdsRecs()

# prod = hnd.getProductById(2)
# print(prod.product_name)
# hnd.removeBatch(prod, 1)

# print(p)
# json_object = json.dumps(p, indent=4)
# print(json_object)
