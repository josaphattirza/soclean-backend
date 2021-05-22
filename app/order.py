class Order:
    # Doesn't include order_id because it is self assigned
    def __init__(self, customer_id, customer_name, address, area, workers_amount, price, payment_method, date, shift, customer_phone, customer_email,manhour, workerIds, order_status):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.workers_amount = workers_amount
        self.price = price
        self.date = date
        self.shift = shift
        self.customer_phone = customer_phone
        self.customer_email = customer_email
        self.address = address
        self.area = area
        self.payment_method = payment_method
        self.order_status = order_status

        self.manhour = manhour
        self.workerIds = workerIds

    def myfunc(self):
        print("Hello my name is " + self.customer_id)

    def __str__(self):
        cid = str(self.customer_id)
        cn = str(self.customer_name)
        wa = str(self.workers_amount)
        p = str(self.price)
        d = str(self.date)
        sh = str(self.shift)
        cp = str(self.customer_phone)
        ce = str(self.customer_email)
        ad = str(self.address)
        ar = str(self.area)
        m = str(self.manhour)
        wid = str(self.workerIds)
        pm = str(self.payment_method)
        os = str(self.order_status)
        return cid + cn + wa + p + sh + d + cp + ce + ad + ar + m + wid + pm + os