import os
import stripe
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Stripe
stripe.api_key = os.getenv("STRIPE_API_KEY")

class StripeService:
    def __init__(self):
        """Initialize Stripe service"""
        self.product_id = os.getenv("STRIPE_PRODUCT_ID")
        
        # Define subscription tiers
        self.subscription_tiers = {
            "basic": {
                "price_id": os.getenv("STRIPE_BASIC_PRICE_ID"),
                "name": "Basic Plan",
                "minutes": 300,
                "price": 9.99  # $9.99 per month
            },
            "pro": {
                "price_id": os.getenv("STRIPE_PRO_PRICE_ID"),
                "name": "Pro Plan",
                "minutes": 1000,
                "price": 19.99  # $19.99 per month
            }
        }
        
    def create_customer(self, user_email, user_name=None):
        """
        Create a new Stripe customer
        
        Args:
            user_email: User's email address
            user_name: User's name (optional)
        
        Returns:
            customer_id: Stripe customer ID
        """
        try:
            customer = stripe.Customer.create(
                email=user_email,
                name=user_name
            )
            
            logger.info(f"Created Stripe customer: {customer.id}")
            
            return customer.id
        
        except stripe.error.StripeError as e:
            logger.error(f"Error creating Stripe customer: {str(e)}")
            raise
            
    def create_subscription(self, customer_id, price_id):
        """
        Create a new subscription for a customer
        
        Args:
            customer_id: Stripe customer ID
            price_id: Stripe price ID
            
        Returns:
            subscription: Stripe subscription object
        """
        try:
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[
                    {"price": price_id},
                ],
                payment_behavior='default_incomplete',
                expand=['latest_invoice.payment_intent'],
            )
            
            logger.info(f"Created Stripe subscription: {subscription.id}")
            
            return {
                "subscription_id": subscription.id,
                "client_secret": subscription.latest_invoice.payment_intent.client_secret,
                "subscription_status": subscription.status
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Error creating Stripe subscription: {str(e)}")
            raise
            
    def cancel_subscription(self, subscription_id):
        """
        Cancel a subscription
        
        Args:
            subscription_id: Stripe subscription ID
            
        Returns:
            success: Boolean indicating if cancellation was successful
        """
        try:
            subscription = stripe.Subscription.delete(subscription_id)
            
            logger.info(f"Cancelled Stripe subscription: {subscription_id}")
            
            return True
            
        except stripe.error.StripeError as e:
            logger.error(f"Error cancelling Stripe subscription: {str(e)}")
            raise
            
    def create_checkout_session(self, customer_id, price_id, success_url, cancel_url):
        """
        Create a checkout session for a customer
        
        Args:
            customer_id: Stripe customer ID
            price_id: Stripe price ID
            success_url: URL to redirect to on successful payment
            cancel_url: URL to redirect to on cancelled payment
            
        Returns:
            session: Stripe checkout session
        """
        try:
            session = stripe.checkout.Session.create(
                customer=customer_id,
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': price_id,
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url=success_url,
                cancel_url=cancel_url,
            )
            
            logger.info(f"Created Stripe checkout session: {session.id}")
            
            return session
            
        except stripe.error.StripeError as e:
            logger.error(f"Error creating Stripe checkout session: {str(e)}")
            raise
            
    def create_portal_session(self, customer_id, return_url):
        """
        Create a Stripe Customer Portal session
        
        Args:
            customer_id: Stripe customer ID
            return_url: URL to return to after portal session
            
        Returns:
            session: Stripe portal session
        """
        try:
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=return_url,
            )
            
            logger.info(f"Created Stripe portal session: {session.id}")
            
            return session
            
        except stripe.error.StripeError as e:
            logger.error(f"Error creating Stripe portal session: {str(e)}")
            raise
            
    def handle_webhook(self, payload, sig_header):
        """
        Handle Stripe webhook events
        
        Args:
            payload: Webhook payload
            sig_header: Stripe signature header
            
        Returns:
            event: Processed Stripe event
        """
        try:
            # Verify webhook signature
            endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
            
            logger.info(f"Received Stripe webhook event: {event.type}")
            
            return event
            
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid Stripe webhook signature: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error handling Stripe webhook: {str(e)}")
            raise 