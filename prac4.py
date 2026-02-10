from collections import defaultdict


class Product:
    def __init__(self, name, price):
        self._name = name
        self._price = price

    def get_name(self):
        return self._name

    def get_price(self):
        return self._price


class Cart:
    def __init__(self):
        self._cart = defaultdict()
        self._total = 0

    def add_product(self, product, quantity):
        if quantity < 1:
            return "invalid quanitity"
        self._cart[product.get_name()] = (quantity, product.get_price())
        self._total += product.get_price() * quantity

    def get_total(self):
        return self._total

    def get_cart(self):
        return self._cart

    def apply_discount(self, discount):
        self._total = discount.apply(self)


class FlatDiscount:
    def __init__(self, discount):
        self._d = discount
        self._amount = 0

    def apply(self, cart):
        self._amount = cart.get_total() - self._d
        if self._amount < 0:
            self._amount = 0
        return self._amount


class PercentageDiscount:
    def __init__(self, discount):
        self._d = discount
        self._amount = 0

    def apply(self, cart):
        self._amount = cart.get_total() - (cart.get_total() * (self._d / 100))
        return self._amount


class BuyOneGetOne:
    def __init__(self, discount):
        self._d = discount
        self._amount = 0

    def apply(self, cart):
        contents = cart.get_cart()
        self._d = 0
        for i in contents.values():
            q, p = i
            if q > 1:
                self._d += p
        self._amount = cart.get_total() - self._d
        return self._amount


class StackedDiscounts:
    def __init__(self):
        self._discounts = []

    def stack_discount(self, discount):
        self._discounts.append(discount)

    def apply(self, cart):
        for i in self._discounts:
            cart.apply_discount(i)
        return cart.get_total()


def main():
    p1 = Product("hat", 10)
    p2 = Product("shoe", 20)

    cart = Cart()
    cart.add_product(p1, 2)
    cart.add_product(p2, 2)

    discount = FlatDiscount(10)
    stack = StackedDiscounts()
    stack.stack_discount(discount)
    stack.stack_discount(discount)
    # d.cash_d(10, cart)
    # d.perc_d(10, cart)
    print(cart.get_total())
    # cart.apply_discount(discount)
    cart.apply_discount(stack)
    print(cart.get_total())


main()
