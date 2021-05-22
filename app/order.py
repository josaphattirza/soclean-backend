class Order:
    # Doesn't include order_id because it is self assigned
    def __init__(self, customerId, customer_name, address, area, workers_amount, price, payment_method, date, shift, customer_phone, customer_email,manhour, workerIds, order_status):
        self.customerId = customerId
        self.customerName = customer_name
        self.workersAmount = workers_amount
        self.price = price
        self.date = date
        self.shift = shift
        self.customerPhone = customer_phone
        self.customerEmail = customer_email
        self.address = address
        self.area = area
        self.paymentMethod = payment_method
        self.orderStatus = order_status

        self.manhour = manhour
        self.workerIds = workerIds

    def myfunc(self):
        print("Hello my name is " + self.customerId)

    def __str__(self):
        cid = str(self.customerId)
        cn = str(self.customerName)
        wa = str(self.workersAmount)
        p = str(self.price)
        d = str(self.date)
        sh = str(self.shift)
        cp = str(self.customerPhone)
        ce = str(self.customerEmail)
        ad = str(self.address)
        ar = str(self.area)
        m = str(self.manhour)
        wid = str(self.workerIds)
        pm = str(self.paymentMethod)
        os = str(self.orderStatus)
        return cid + cn + wa + p + sh + d + cp + ce + ad + ar + m + wid + pm + os