def calculate_total(cart_items):

    total = 0

    for item in cart_items:

        total += item.quantity * item.product.price

    return total
