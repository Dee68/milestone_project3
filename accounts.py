class Account:
    """Blue print of a bank account of a customer
    """

    def __init__(self, acc_num, first_name, last_name, pin, balance):
        """ Creates an instance of the class Account """
        self._acc_num = acc_num
        self._first_name = first_name
        self._last_name = last_name
        self._pin = pin
        self._balance = balance

    def __str__(self):
        """ Returns a human readable pattern of the instance."""
        p_1 = self._acc_num
        p_2 = self.first_name
        p_3 = self.last_name
        p_4 = self.pin
        p_5 = self.balance
        return f"Account({p_1},{p_2},{p_3},{p_4},{p_5})"

    # Getter methods
    @property
    def acc_num(self):
        """ gets account number """
        return self._acc_num

    @property
    def first_name(self):
        """ gets card holder last name"""
        return self._first_name

    @property
    def last_name(self):
        """ gets card holder last name"""
        return self._last_name

    @property
    def pin(self):
        """ gets card holder pin code """
        return self._pin

    @property
    def balance(self):
        """ gets card holder balance """
        return self._balance

    # Setter methods
    @acc_num.setter
    def acc_num(self, new_value):
        """ sets the account number of the account """
        self._acc_num = new_value

    @first_name.setter
    def first_name(self, new_value):
        """ sets the account holder first name """
        self._first_name = new_value

    @last_name.setter
    def last_name(self, new_value):
        """ sets the account holder last name """
        self._last_name = new_value

    @pin.setter
    def pin(self, new_value):
        """ sets the account holder PIN """
        self._pin = new_value

    @balance.setter
    def balance(self, new_value):
        """ sets the account  balance """
        self._balance = new_value
