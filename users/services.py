import os
import stripe
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("API_KEY_STRIPE")

def create_session(price):
  session = stripe.checkout.Session.create(
  success_url="http://127.0.0.1:8000/success",
  line_items=[{"price": price.id, "quantity": 1}],
  mode="payment",
  )
  return session.id, session.url

def create_price(course, amount):
  product = create_product(course)
  price = stripe.Price.create(
  currency="rub",
  unit_amount=int(amount*100),
  product_data={"name": product.id},
  )
  return price

def create_product(course):
  return stripe.Product.create(name=course)

