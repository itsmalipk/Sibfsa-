from dataclasses import dataclass
from typing import Dict
from .models import Product

CART_SESSION_KEY = 'cart'

@dataclass
class CartItem:
  product: Product
  quantity: int

def _get(session) -> Dict[str,int]: return session.get(CART_SESSION_KEY, {})
def _save(session, cart: Dict[str,int]):
  session[CART_SESSION_KEY] = cart
  session.modified = True

def add(session, product_id:int, qty:int=1):
  cart = _get(session); key = str(product_id)
  cart[key] = cart.get(key, 0) + max(1, qty)
  _save(session, cart)

def remove(session, product_id:int):
  cart = _get(session); cart.pop(str(product_id), None); _save(session, cart)

def set_qty(session, product_id:int, qty:int):
  cart = _get(session); key = str(product_id)
  if qty <= 0: cart.pop(key, None)
  else: cart[key] = qty
  _save(session, cart)

def items_and_total(session):
  cart = _get(session)
  ids = [int(pid) for pid in cart.keys()]
  products = {p.id: p for p in Product.objects.filter(id__in=ids).prefetch_related('images')}
  items = []; total = 0
  for pid_str, qty in cart.items():
    p = products.get(int(pid_str))
    if not p: continue
    total += p.price_pkr * qty
    items.append(CartItem(product=p, quantity=qty))
  return items, total