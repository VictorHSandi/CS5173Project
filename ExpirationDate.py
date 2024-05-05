import datetime

## Class to periodically check the key's expiration status 
class ExpirationDate:

    ## variables: initial date of key, frequency key is to be updated, set expiration date
    def __init__(self, initDate, updateFreq):
        self.initDate = initDate
        self.updateFreq = updateFreq
        self.expDate = initDate #initializing, value to be changed

    ## incrementing initial date by user specified frequency
    def genExpDate(self):
        self.expDate += datetime.timedelta(days = self.updateFreq)
        return self.expDate

    def is_expired(self):
        if (self.expDate <= datetime.datetime.now()):
            return True
        else:
            return False