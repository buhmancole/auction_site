from django.core.management.base import BaseCommand
from auction.models import *
from django.core.files import File
from django.utils.timezone import make_aware
from datetime import datetime
import random

class Command(BaseCommand):
    help = 'Produces x auctions with y objects'


    def handle(self, *args, **options):
        self.init(options['auctions'][0], options['objects'][0])

    def add_arguments(self, parser):
        parser.add_argument('auctions', nargs='+', type=int)
        parser.add_argument('objects', nargs='+', type=int)


    def init(self, auctions, objects):
        self.DEFAULT_PRICE = 10
        #Clear out the database
        Bidder.objects.all().delete()
        Auction.objects.all().delete()
        Item.objects.all().delete()
        Bid.objects.all().delete()
        Image.objects.all().delete()

        #make an admin
        Bidder.objects.create_superuser(username="admin",  password="admin");

        for i in range(auctions):
            print(f"making auction {i}")
            auction = self.newAuction(i)
            for j in range(objects):
                bidder = self.newBidder(i,j, auction)
                item = self.newItem(j, auction)
                if i>0:
                    bid = self.newBid(bidder, j, item)
                bidder.addFavorite(item)
            item = self.newItem(objects, auction, True)

        print(f"""
Done!
{auctions} auctions were created, each has passphrase 'test0' (test1, test2, etc.)
{objects} bidders, items, and bids were created in each auction. Each bidder's username is bidder[auctionnumber].[number]@test.com (bidder0.0@test.com, bidder0.1@test.com, etc.) and have the standard password 'testing'.
One admin was created, with username and password 'admin'.
Each item has 3 test images associated with it.
The first auction has had no bids placed.
            """)


    def newAuction(self, number):
        auction = Auction(_passphrase=f'test{number}')
        auction.changeName(f"Test Auction {number}")
        auction.changeStart(make_aware(datetime(2020,3,10,0,0,0)))
        auction.changeEnd(make_aware(datetime(2020,5,10+number,number,number,number)))
        auction.save()
        return auction


    def newItem(self, number, auction, isLive=False):
        item = Item()
        item.changeName(f"Sample Item {number}")
        item.changeDesc(f"This is a sample item #{number}")
        item.changePrice(self.DEFAULT_PRICE)
        item.changeIsLive(isLive)
        item.changeAuction(auction)
        item.changeCategory(random.choice(list(Item.Categories)))
        item.save()
        for i in range(3):
            self.newImage(item, f"test{number}_{i}.jpg")
        return item


    def newBid(self, bidder, amount, item):
        bid = Bid(_bidPrice=self.DEFAULT_PRICE+2+amount, _bidder=bidder, _item=item)
        bid.save()
        return bid

    def newBidder(self, auctionNumber, number, auction):
        bidder = Bidder()
        bidder.first_name = "Test"
        bidder.last_name = f"Bidder {number}"
        bidder.email = f"bidder{auctionNumber}.{number}@test.com"
        bidder.set_password("testing")
        bidder.save()
        bidder.addAuction(auction)
        bidder.save()
        return bidder


    def newImage(self, item, imagename):
        image = Image(_item=item)
        image._image.save(f'{imagename}', File(open(f'alphaAuction/auction/static/auction/testImgs/{imagename}', 'rb')))
        image.save()
        return image


