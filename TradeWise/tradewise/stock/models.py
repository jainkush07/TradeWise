from django.db import models
# from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    # Add any additional fields you want to store for your app's users
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)

    # Set a unique related_name for the groups and user_permissions fields
    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name="custom_users"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name="custom_users"
    )

class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.symbol} - {self.name}"

class FundamentalAnalysis(models.Model):
    stock = models.OneToOneField(Stock, on_delete=models.CASCADE)
    market_cap = models.FloatField()
    pe_ratio = models.FloatField()
    dividend_yield = models.FloatField()
    # Add more fundamental analysis fields as needed

    def __str__(self):
        return f"Fundamental Analysis for {self.stock}"

class SentimentAnalysis(models.Model):
    stock = models.OneToOneField(Stock, on_delete=models.CASCADE)
    sentiment_score = models.FloatField()
    news_headline = models.TextField()
    # Add more sentiment analysis fields as needed

    def __str__(self):
        return f"Sentiment Analysis for {self.stock}"

class TechnicalAnalysis(models.Model):
    stock = models.OneToOneField(Stock, on_delete=models.CASCADE)
    moving_average = models.FloatField()
    rsi = models.FloatField()
    # Add more technical analysis fields as needed

    def __str__(self):
        return f"Technical Analysis for {self.stock}"
    

class Trade(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    entry_price = models.FloatField()
    exit_price = models.FloatField(null=True, blank=True)
    entry_date = models.DateField()
    exit_date = models.DateField(null=True, blank=True)
    # Add more trade-related fields as needed

    def __str__(self):
        return f"Trade for {self.stock}"

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stocks = models.ManyToManyField(Stock, through='PortfolioStock')
    # Add more portfolio-related fields as needed

    def __str__(self):
        return f"Portfolio for {self.user}"

class PortfolioStock(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    average_price = models.FloatField()
    # Add more portfolio stock-related fields as needed

    def __str__(self):
        return f"Stock {self.stock} in Portfolio {self.portfolio}"
