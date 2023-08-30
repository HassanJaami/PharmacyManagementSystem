# from DB_Admin import AdminDBHndler
# from DB_Pharmacist import PharmacistDBHndler

from DB_Handler import DBHandler


class Login:
    def __init__(self):
        self.hndler = DBHandler()

    # recives 'userId'
    # returns string corresponding to account type, if it is valid 'userId'
    # return false, if invalid 'userId'
    def getAccType(self, userId):
        obj = self.hndler.getAdmin(userId)
        if obj:
            return 'admin'
        obj = self.hndler.getPharmacist(userId)
        if obj:
            return 'pharmacist'
        return False

    # both functions validate respective account-id passwords
    # if valid password return True
    def validateAdminPassword(self, id, pswd):
        if pswd == self.hndler.getAdminPass(id):
            return True
        return False

    def validatePharmacistPassword(self, id, pswd):
        if pswd == self.hndler.getPharmPass(id):
            return True
        return False
