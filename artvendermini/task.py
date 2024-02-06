# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from .models import User_Bid, AuctionItem
from django.utils import timezone

@shared_task
def check_auction_end():
    current_time = timezone.now()
    auctions = AuctionItem.objects.filter(end_date__lte=current_time, is_active=True)

    for auction in auctions:
        winning_bid = User_Bid.objects.filter(auction_item=auction).order_by('-bid_price').first()

        if winning_bid:
            winning_bid.is_approved = True
            winning_bid.save()

            subject = 'Congratulations! You won the auction'
            message = f'Dear {winning_bid.buyer.username},\n\nYou have won the auction for {winning_bid.auction_item.name} with a bid of {winning_bid.bid_price}. Thank you for participating!'
            from_email = 'your_email@example.com'
            to_email = [winning_bid.buyer.email]
            send_mail(subject, message, from_email, to_email, fail_silently=False)

        # Mark the auction as inactive
        auction.is_active = False
        auction.save()
