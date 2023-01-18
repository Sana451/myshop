import stripe
stripe.api_key = "sk_test_51MOu2hBEIv7j3XF3ZZwclG2ekgfUpNEIpFH9WqdaMnPaLhWfTh3omttdqv2iNqItciFneZ9ubsSmUsz9RhTWQjaz007PbUX3oQ"

starter_subscription = stripe.Product.create(
  name="Starter Subscription",
  description="$12/Month subscription",
)

starter_subscription_price = stripe.Price.create(
  unit_amount=1200,
  currency="usd",
  recurring={"interval": "month"},
  product=starter_subscription['id'],
)

# Save these identifiers
print(f"Success! Here is your starter subscription product id: {starter_subscription.id}")
print(f"Success! Here is your starter subscription price id: {starter_subscription_price.id}")

# prod_NAAWPARpI6H8M7  ---  product id
# price_1MPqBpBEIv7j3XF3mYrqOg4H --- price id