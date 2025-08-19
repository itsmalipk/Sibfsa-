def theme_and_cart(request):
    theme = request.COOKIES.get('theme', 'light')
    cart = request.session.get('cart', {})
    return {
        'theme': theme,
        'theme_class': 'theme-dark' if theme == 'dark' else '',
        'cart_count': sum(cart.values())
    }