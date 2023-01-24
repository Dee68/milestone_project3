class Account:
    """ Blue print of a bank account of a customer"""

    def __init__(self, acc_num, first_name, last_name, pin, balance):
        """ Creates an instance of the class Account """
        self._acc_num = acc_num
        self.first_name = first_name
        self.last_name = last_name
        self.pin = pin
        self.balance = balance

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

    def get_first_name(self):
        """ gets card holder last name"""
        return self.first_name

    def get_last_name(self):
        """ gets card holder last name"""
        return self.last_name

    def get_pin(self):
        """ gets card holder pin code """
        return self.pin

    def get_balance(self):
        """ gets card holder balance """
        return self.balance

    # Setter methods
    @acc_num.setter
    def set_acc_num(self, new_value):
        """ sets the account number of the account """
        self._acc_num = new_value

    def set_first_name(self, new_value):
        """ sets the account holder first name """
        self.first_name = new_value

    def set_last_name(self, new_value):
        """ sets the account holder last name """
        self.last_name = new_value

    def set_pin(self, new_value):
        """ sets the account holder PIN """
        self.pin = new_value

    def set_balance(self, new_value):
        """ sets the account  balance """
        self.balance = new_value
