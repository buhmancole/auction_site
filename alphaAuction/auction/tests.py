from django.core.exceptions import ValidationError
from django.test import TestCase
from datetime import datetime
from auction.models import *
from django.core.files import File
from django.utils.timezone import make_aware


class BidderTestCase(TestCase):
    '''
    Attributes:
        _auctions: auction
        _favorites: items
        _resetHash: String
        _columns: int
        first_name: String
        last_name: String
        password: String
        email: Email
        _currentAuction: auction
    Methods:
        getColumns: int
        changeColumns(int): bool
        getFavorites: list of items
        addFavorite(item): bool
        removeFavorite(item): bool
        getCurrentFavorites(): list of items
        changeCurrentAuction(auction): bool
        getCurrentAuction(): auction
        getFullName: String
        getLastName: String
        changeFirstName(String): bool
        changeLastName(String): bool
        addAuction(auction): bool
        changePassword(String): bool
        getEmail: Email
        getAuctions: list of auctions
        getAmountOwed: int
        getItemsBidOn: list of items
        getItemsWinning: list of items
        generateResetHash: hash
    '''
    def setUp(self):
        bidder1 = Bidder(first_name='kai',last_name='jameson',  password='kaiPassword123', email='kai@gmail.com')
        bidder1.save()
        bidder2 = Bidder(first_name='avery!!!',last_name='b0bio', password='this one is a secret ;)', email='avery@avery.org')
        bidder2.save()
        auction = Auction(_name='default auction', _passphrase='defaultauctionpassphrase',
                          _startTime=make_aware(datetime(2020, 3, 20, 0, 0, 0)),
                          _endTime=make_aware(datetime(2020, 5, 22, 0, 0, 0)))
        auction.save()
        bidder3 = Bidder(first_name='best',last_name='ever', password='iruletheworld', email='canttouch@this.com', _currentAuction=auction)
        bidder3.save()
        item = Item(_auction=auction, _minIncrement=1, _currentPrice=2, _name='bike',
                    _description='it has wheels', _isLive=False)
        item.save()
        item2 = Item(_auction=auction, _minIncrement=1, _currentPrice=4, _name='cow',
                    _description='it has utters', _isLive=False)
        item2.save()
        bid = Bid(_bidder=bidder1, _bidPrice=3, _item=item)
        bid.save()
        bid2 = Bid(_bidder=bidder1, _bidPrice=6, _item=item2)
        bid2.save()

    def test_hasEmail(self):
        bidder = Bidder.objects.get(pk=1)
        self.assertEqual(bidder.getEmail(), 'kai@gmail.com')

    def test_addAuction(self):
        bidder = Bidder.objects.get(pk=1)
        auction = Auction(_name='tooearly', _passphrase='bidnotbegin',
                          _startTime=make_aware(datetime(2020, 5, 20, 0, 0, 0)),
                          _endTime=make_aware(datetime(2020, 5, 22, 0, 0, 0)))
        auction.save()
        auction = Auction.objects.get(_name='tooearly')
        self.assertTrue(bidder.addAuction(auction))

    def test_canChangeEmail(self):
        bidder = Bidder.objects.get(pk=1)
        self.assertTrue(bidder.changeEmail('kaiIsTheBest@bestever.com')) 
        self.assertTrue(bidder.changeEmail('kai@gmail.com')) #email can be changed to itself
        self.assertTrue(bidder.changeEmail('KAI@GMAIL.COM')) #email can be changed to itself, case insensitive
        bidder.save()
        bidder = Bidder.objects.get(pk=1)
        self.assertEqual(bidder.getEmail(), 'kai@gmail.com') #the email actually changed

    def test_invalidEmail(self):
        bidder = Bidder.objects.get(pk=1)
        self.assertFalse(bidder.changeEmail('not a valid email')) #email must be a valid email format
        self.assertFalse(bidder.changeEmail('avery@avery.org')) #email must be unique from other bidders
        self.assertFalse(bidder.changeEmail('AVERY@AVERY.ORG')) #email must be unique from other bidders, case insensitive
        self.assertRaises(ValidationError, bidder.save)
        email = bidder.getEmail()
        self.assertEqual(bidder.getEmail(), email) #email didn't actually change

    def test_hasFirstName(self):
        bidder = Bidder.objects.get(pk=1)
        self.assertEqual(bidder.getFirstName(), 'kai')

    def test_hasLastName(self):
        bidder = Bidder.objects.get(pk=1)
        self.assertEqual(bidder.getLastName(), 'jameson')

    def test_hasFullName(self):
        bidder = Bidder.objects.get(pk=1)
        self.assertEqual(bidder.getFullName(), 'kai jameson')

    def test_canChangeFirstName(self):
        bidder = Bidder.objects.get(pk=1)
        self.assertTrue(bidder.changeFirstName('Kai'))
        bidder.save()
        bidder = Bidder.objects.get(pk=1)
        self.assertEqual(bidder.getFirstName(), 'Kai')

    def test_canChangeLastName(self):
        bidder = Bidder.objects.get(pk=1)
        self.assertTrue(bidder.changeLastName('Jameson'))
        bidder.save()
        bidder = Bidder.objects.get(pk=1)
        self.assertEqual(bidder.getLastName(), 'Jameson')

    def test_canChangePassword(self):
        bidder = Bidder.objects.get(pk=1)
        self.assertTrue(bidder.changePassword('passKai123'))
        bidder.save()
        bidder = Bidder.objects.get(pk=1)
        self.assertTrue(bidder.check_password('passKai123'))

    def test_passwordTooShort(self):
        bidder = Bidder.objects.get(pk=1)
        self.assertFalse(bidder.changePassword('kai'))
        bidder.save()
        bidder = Bidder.objects.get(pk=1)
        self.assertFalse(bidder.check_password('kai'))

    def test_passwordTooLong(self):
        bidder = Bidder.objects.get(pk=1)
        self.assertFalse(bidder.changePassword('kaithispasswordwillnotworkitisdefinatelymorethan20characters'))
        bidder.save()
        bidder = Bidder.objects.get(pk=1)
        self.assertFalse(bidder.check_password('kaithispasswordwillnotworkitisdefinatelymorethan20characters'))

    def test_getAmountOwed(self):
        bidder = Bidder.objects.get(pk=1)
        self.assertEqual(bidder.getAmountOwed(), 9)

    def test_getAmountOwedWithNoBids(self):
        bidder = Bidder.objects.get(pk=2)
        self.assertEqual(bidder.getAmountOwed(), 0)

    def test_getItemsBidOn(self):
        bidder = Bidder.objects.get(pk=1)
        ids = []
        for i in range(1,3):
            item = Item.objects.get(pk=i)
            ids.append(item.id)
        items = bidder.getItemsBidOn()
        for x in range(0,2):
            self.assertEqual(items[x].id, ids[x])

    def test_getItemsWinning(self):
        bidder = Bidder.objects.get(pk=1)
        bidder2 = Bidder.objects.get(pk=2)
        itemToOutbid = Item.objects.get(pk=2)
        outbid = Bid(_bidder=bidder2, _bidPrice=12, _item=itemToOutbid)
        outbid.save()
        itemWinning = Item.objects.get(pk=1)
        items = bidder.getItemsWinning()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].id, itemWinning.id)

    def test_canGetCurrentAuction(self):
        auction = Auction.objects.get(pk=1)
        bidder = Bidder.objects.get(pk=3)
        self.assertEqual(auction.id, bidder.getCurrentAuction().id)

    def test_canAddCurrentAuction(self):
        bidder = Bidder.objects.get(pk=1)
        auction = Auction.objects.get(pk=1)
        self.assertTrue(bidder.changeCurrentAuction(auction))
        bidder = Bidder.objects.get(pk=1)
        self.assertEqual(auction.id, bidder.getCurrentAuction().id)

    def test_canAddFavorite(self):
        bidder = Bidder.objects.get(pk=1)
        item = Item.objects.get(pk=1)
        self.assertTrue(bidder.addFavorite(item))

    def test_canGetFavorite(self):
        bidder = Bidder.objects.get(pk=1)
        item = Item.objects.get(pk=1)
        self.assertTrue(bidder.addFavorite(item))
        bidder = Bidder.objects.get(pk=1)
        favorites = bidder.getFavorites()
        self.assertEqual(len(favorites), 1)
        self.assertEqual(favorites[0].id, item.id)

    def test_canRemoveFavorite(self):
        bidder = Bidder.objects.get(pk=1)
        item = Item.objects.get(pk=1)
        self.assertTrue(bidder.addFavorite(item))
        bidder = Bidder.objects.get(pk=1)
        favorites = bidder.getFavorites()
        self.assertEqual(len(favorites), 1)
        self.assertTrue(bidder.removeFavorite(item))
        bidder = Bidder.objects.get(pk=1)
        updatedFavorites = bidder.getFavorites()
        self.assertEqual(len(updatedFavorites), 0)

    def test_canGetCurrentFavorites(self):
        bidder = Bidder.objects.get(pk=3)
        item = Item.objects.get(pk=1)
        auction = Auction(_name='woot', _passphrase='thenextbest',
                          _startTime=make_aware(datetime(2020, 3, 10, 0, 0, 0)),
                          _endTime=make_aware(datetime(2020, 5, 12, 0, 0, 0)))
        auction.save()
        item2 = Item(_auction=auction, _currentPrice=4, _name='bird',_description='it sings')
        item2.save()
        item2 = Item.objects.get(_name='bird')
        self.assertTrue(bidder.addFavorite(item))
        self.assertTrue(bidder.addFavorite(item2))
        bidder = Bidder.objects.get(pk=3)
        currFavorites = bidder.getCurrentFavorites()
        self.assertTrue(item in currFavorites)
        self.assertFalse(item2 in currFavorites)




class AuctionTestCase(TestCase):
    '''
    Attributes:
        _startTime: timestamp
        _endTime: timeStamp
        _name: String
        _passphrase: String
    Methods:
        isRunning: bool
        getStart: timestamp
        getEnd: timestamp
        containsBidder(bidder): bool
        changeStart(timestamp): bool
        changeEnd(timestamp): bool
        getBidders: list of bidders
        getItems: list of items
        getLiveItems: list of live items
        getSilentItems: list of silent items
        getPass: String
        getName: String
        changePass(String): bool
        changeName(String): bool
        changeEnd(timestamp): bool
        getEarnings: int
        getWinners: list of bidders
    '''
    def setUp(self):
        auction = Auction(_name='default auction', _passphrase='defaultpassphrase',
                          _startTime=make_aware(datetime(2020,3,20,0,0,0)), _endTime=make_aware(datetime(2020,5,22,0,0,0)))
        auction.save()
        bidder1 = Bidder(first_name='Kai', last_name='Jameson', password='kaiPassword123', username='kaiJ@gmail.com',
                        email='kaiJ@gmail.com')
        bidder1.save()
        bidder2 = Bidder(first_name='john', last_name='smith', password='jsmith12', username='jsmith@gmail.com',
                        email='jsmith@gmail.com')
        bidder2.save()
        bidder3 = Bidder(first_name='harry', last_name='potter', password='hpotter7', username='hpotter@gmail.com',
                         email='hpotter@gmail.com')
        bidder3.save()
        item = Item(_auction=auction, _minIncrement=1, _currentPrice=2, _name='bike',
                    _description='it has wheels', _isLive=False)
        item.save()
        item2 = Item(_auction=auction, _minIncrement=4, _currentPrice=17, _name='cow',
                     _description='it has utters', _isLive=False)
        item2.save()

    def test_hasName(self):
        auction = Auction.objects.get(pk=1)
        self.assertEqual(auction.getName(), 'default auction')

    def test_canChangeName(self):
        auction = Auction.objects.get(pk=1)
        self.assertTrue(auction.changeName('not default'))
        auction.save()
        auction = Auction.objects.get(pk=1)
        self.assertEqual(auction.getName(), 'not default')

    def test_hasPass(self):
        auction = Auction.objects.get(pk=1)
        self.assertEqual(auction.getPass(), 'defaultpassphrase')

    def test_canChangePass(self):
        auction = Auction.objects.get(pk=1)
        self.assertTrue(auction.changePass('newpassphrase'))
        auction.save()
        auction = Auction.objects.get(pk=1)
        self.assertEqual(auction.getPass(), 'newpassphrase')

    def test_cantMakeAuctionWithPassWithSpace(self):
        auction = Auction(_name='failed auction', _passphrase='has a space',
                          _startTime=make_aware(datetime(2020, 3, 20, 0, 0, 0)),
                          _endTime=make_aware(datetime(2020, 5, 22, 0, 0, 0)))
        self.assertRaises(ValidationError, auction.save)

    def test_cantChangePassWithSpace(self):
        auction = Auction.objects.get(pk=1)
        passphrase = auction.getPass()
        self.assertFalse(auction.changePass('no spaces allowed')) #note that although it will not be able to save, the object still has the invalid password
        self.assertRaises(ValidationError, auction.save)
        #verify that the one in the database did NOT change
        auction = Auction.objects.get(pk=1)
        self.assertEqual(auction.getPass(), passphrase)

    def test_hasStartTime(self):
        auction = Auction.objects.get(pk=1)
        self.assertEqual(auction.getStart(), make_aware(datetime(2020,3,20,0,0,0)))

    def test_hasEndTime(self):
        auction = Auction.objects.get(pk=1)
        self.assertEqual(auction.getEnd(), make_aware(datetime(2020,5,22,0,0,0)))

    def test_changeStartTime(self):
        auction = Auction.objects.get(pk=1)
        self.assertTrue(auction.changeStart(make_aware(datetime(2020, 3, 21, 0, 0, 0))))
        self.assertEqual(auction.getStart(), make_aware(datetime(2020, 3, 21, 0, 0, 0)))

    def test_changeEndTime(self):
        auction = Auction.objects.get(pk=1)
        self.assertTrue(auction.changeEnd(make_aware(datetime(2020, 5, 2, 0, 0, 0))))
        self.assertEqual(auction.getEnd(), make_aware(datetime(2020, 5, 2, 0, 0, 0)))

    def test_startCannotBeAfterEnd(self):
        auction = Auction.objects.get(pk=1)
        startTime = auction.getStart()
        self.assertFalse(auction.changeStart(make_aware(datetime(2021, 3, 21, 0, 0, 0))))
        self.assertRaises(ValidationError, auction.save)
        auction = Auction.objects.get(pk=1)
        self.assertEqual(auction.getStart(), startTime)

    def test_cantMakeAuctionWithStartAfterEnd(self):
        auction2 = Auction(_name="timeTest", _passphrase="Cantmake",
                           _startTime=make_aware(datetime(2021, 3, 20, 0, 0, 0)),
                           _endTime=make_aware(datetime(2020, 3, 20, 0, 0, 0)))
        self.assertRaises(ValidationError, auction2.save)

    def test_getBidders(self):
        ids = []
        auction = Auction.objects.get(pk=1)
        for i in range(1, 4):
            bidder = Bidder.objects.get(pk=i)
            bidder.addAuction(auction)
            ids.append(bidder.id)
        updatedAuction = Auction.objects.get(pk=1)
        bidders = updatedAuction.getBidders()
        for x in range(0,3):
            self.assertEqual(bidders[x].id, ids[x])

    def test_containsBidder(self):
        auction = Auction.objects.get(pk=1)
        bidder1 = Bidder.objects.get(pk=1)
        bidder1.addAuction(auction)
        updatedAuction = Auction.objects.get(pk=1)
        bidder2 = Bidder.objects.get(pk=2)
        self.assertTrue(updatedAuction.containsBidder(bidder1))
        self.assertFalse(updatedAuction.containsBidder(bidder2))

    def test_getItems(self):
        ids = []
        for i in range(1,3):
            item = Item.objects.get(pk=i)
            ids.append(item.id)
        auction = Auction.objects.get(pk=1)
        items = auction.getItems()
        for x in range(0,2):
            self.assertEqual(items[x].id, ids[x])


class ItemTestCase(TestCase):
    '''
    Attributes:
        _name: String
        _description: String
        _isLive: bool: default false
        _currentPrice: int
        _minIncrement: int: default 1
        _auction: auction
        _category: Item.Categories
    Methods:
        getCategory: category
        changeCategory(category): bool
        getWinner: bidder
        getAuction: auction
        changeAuction(auction): bool
        changeDesc(String): bool
        changeMinIncrement(int): bool
        changeIsLive(bool): bool
        getIsLive: bool
        getDesc: String
        changeName(String): bool
        getName: String
        getImages: list of images
        getPrice: int
        getWorth: int
        changePrice(int): bool
        getMinIncrement: int
        getBids: list of bids
    '''
    def setUp(self):
        auction = Auction(_name='default auction', _passphrase='defaultauctionpassphrase',
                          _startTime=make_aware(datetime(2020, 3, 20, 0, 0, 0)),
                          _endTime=make_aware(datetime(2020, 5, 22, 0, 0, 0)))
        auction.save()
        auction2 = Auction(_name="timeTest", _passphrase="Cantmake",
                           _startTime=make_aware(datetime(2020, 3, 29, 0, 0, 0)),
                           _endTime=make_aware(datetime(2020, 5, 2, 0, 0, 0)))
        auction2.save()
        bidder = Bidder(first_name='Kai',last_name='Jameson', password='kaiPassword123', username='kaiJ@gmail.com', email='kaiJ@gmail.com')
        bidder.save()
        item = Item(_auction=auction, _minIncrement=1, _currentPrice=2, _name='bike',
                    _description='it has wheels', _isLive=False)
        item.save()
        item2 = Item(_auction=auction, _minIncrement=4, _currentPrice=17, _name='cow',
                    _description='it has utters', _isLive=False)
        item2.save()
        item3 = Item(_auction=auction, _currentPrice=2, _name='category tester',
                    _description='it has a category', _category=Item.Categories.SCHOOL_SUPPLIES)
        item3.save()
        bid=Bid(_bidder=bidder, _item=item, _bidPrice=2)
        bid.save()
        bid3=Bid(_bidder=bidder, _item=item3, _bidPrice=2)
        bid3.save()

    def test_hasName(self):
        item = Item.objects.get(pk=1)
        self.assertEqual(item.getName(), 'bike')

    def test_hasDescription(self):
        item = Item.objects.get(pk=1)
        self.assertEqual(item.getDesc(), 'it has wheels')

    def test_hasGetPrice(self):
        item = Item.objects.get(pk=1)
        bid = Bid(_bidder=Bidder.objects.get(pk=1), _bidPrice=4, _item=item)
        bid.save()
        self.assertEqual(item.getPrice(), 4)

    def test_getWinner(self):
        item = Item.objects.get(pk=1)
        bidder = Bidder.objects.get(pk=1)
        bid = Bid(_bidder=bidder, _bidPrice=4, _item=item)
        bid.save()
        self.assertEqual(item.getWinner().id, bidder.id)

    def test_getWorth(self):
        item = Item.objects.get(pk=1)
        bidder = Bidder.objects.get(pk=1)
        bid = Bid(_bidder=bidder, _bidPrice=4, _item=item)
        bid.save()
        self.assertEqual(item.getWorth(), 4)

    def test_getWorthWithNoBids(self):
        item = Item.objects.get(pk=2)
        self.assertEqual(item.getWorth(), 0)

    def test_getWinnerWithNoBids(self):
        item = Item.objects.get(pk=2)
        self.assertEqual(item.getWinner(), None)

    def test_canChangeDescription(self):
        item = Item.objects.get(pk=1)
        self.assertTrue(item.changeDesc('i am just a humble item, mate'))
        item.save()
        item = Item.objects.get(pk=1)
        self.assertEqual(item.getDesc(), 'i am just a humble item, mate')

    def test_hasIsLive(self):
        item = Item.objects.get(pk=1)
        self.assertFalse(item.getIsLive())

    def test_canChangeIsLive(self):
        item = Item.objects.get(pk=1)
        self.assertTrue(item.changeIsLive(True))
        item.save()
        item = Item.objects.get(pk=1)
        self.assertTrue(item.getIsLive())

    def test_canChangeName(self):
        item = Item.objects.get(pk=1)
        self.assertTrue(item.changeName('trident'))
        item.save()
        item = Item.objects.get(pk=1)
        self.assertEqual(item.getName(), 'trident')

    def test_getAuction(self):
        auction = Auction.objects.get(pk=1)
        item = Item.objects.get(pk=1)
        self.assertEqual(item.getAuction().id, auction.id)

    def test_canChangeAuction(self):
        item = Item.objects.get(pk=1)
        auction2 = Auction.objects.get(pk=2)
        self.assertTrue(item.changeAuction(auction2))
        self.assertEqual(item.getAuction().id, auction2.id)

    def test_hasCategory(self):
        item = Item.objects.get(_name='category tester')
        self.assertEqual(item.getCategory(), 'SS')

    def test_changeCategory(self):
        item = Item.objects.get(_name='category tester')
        self.assertTrue(item.changeCategory(Item.Categories.TOY))
        item.save()
        item1 = Item.objects.get(_name='category tester')
        self.assertEqual(item1.getCategory(), 'TY')

    def test_hasGetMinIncrement(self):
        item = Item.objects.get(pk=1)
        self.assertEqual(item.getMinIncrement(), 1)

    def test_changeMinIcrement(self):
        item = Item.objects.get(pk=1)
        self.assertTrue(item.changeMinIncrement(4))
        item.save()
        item = Item.objects.get(pk=1)
        self.assertEqual(item.getMinIncrement(), 4)
        self.assertFalse(item.changeMinIncrement(0))
        item = Item.objects.get(pk=1)
        self.assertEqual(item.getMinIncrement(), 4)
        item.save()
        self.assertFalse(item.changeMinIncrement(-1))
        item = Item.objects.get(pk=1)
        self.assertEqual(item.getMinIncrement(), 4)

    def test_cantHaveMinIcrementBeZeroOrNegative(self):
        auction = Auction.objects.get(pk=1)
        item = Item(_auction=auction, _minIncrement=-1, _currentPrice=2, _name='dog',
                    _description='it woofs')
        self.assertRaises(ValidationError, item.save)
        item1 = Item(_auction=auction, _minIncrement=0, _currentPrice=2, _name='dog',
                    _description='it woofs')
        self.assertRaises(ValidationError, item1.save)

    def test_cantHaveCurrentPriceNegative(self):
        auction = Auction.objects.get(pk=1)
        item = Item(_auction=auction, _currentPrice=-1, _name='cat',
                    _description='it meows')
        self.assertRaises(ValidationError, item.save)

    def test_changePrice(self):
        item = Item.objects.get(pk=1)
        self.assertTrue(item.changePrice(100))
        item.save()
        item = Item.objects.get(pk=1)
        self.assertEqual(item.getPrice(), 100)
        self.assertFalse(item.changePrice(-1))
        item = Item.objects.get(pk=1)
        self.assertEqual(item.getPrice(), 100)

    def test_getImages(self):
        item = Item.objects.get(pk=1)
        image = Image(_item=item)
        image._image.save('test', File(open('alphaAuction/auction/static/auction/testImgs/test0_0.jpg', 'rb')))
        image.save()
        item = Item.objects.get(pk=1)
        images = item.getImages()
        for image in images:
            self.assertTrue(image.getImage().url.index('/media/test') > -1)


class BidTestCase(TestCase):
    '''
    Attributes:
        _bidder: bidder
        _bidPrice: int
        _item: item
        _timestamp: timestamp
    Methods:
        getBidder: bidder
        getItem: item
        getPrice: int
        getTime: timestamp
    '''
    def setUp(self):
        auction = Auction(_name='default auction', _passphrase='defaultauctionpassphrase',
                          _startTime=make_aware(datetime(2020, 3, 20, 0, 0, 0)),
                          _endTime=make_aware(datetime(2020, 5, 22, 0, 0, 0)))
        auction.save()
        bidder = Bidder(first_name='john', last_name='smith', password='kaiPassword123', email='kai@gmail.com')
        bidder.save()
        item = Item(_auction=auction, _minIncrement=2, _currentPrice=2, _name='cow',
                    _description='it has utters', _isLive=False)
        item.save()
        item2 = Item(_auction=auction, _minIncrement=4, _currentPrice=17, _name='pig',
                     _description='come get pork', _isLive=False)
        item2.save()
        bid = Bid(_bidder=bidder, _bidPrice=4, _item=item)
        bid.save()

    def test_getBidder(self):
        bid = Bid.objects.get(pk=1)
        bidder = Bidder.objects.get(first_name='john')
        self.assertTrue(bid.getBidder(), bidder)

    def test_getItem(self):
        bid = Bid.objects.get(pk=1)
        item = Item.objects.get(_name='cow')
        self.assertTrue(bid.getItem(), item)

    def test_getPrice(self):
        bid = Bid.objects.get(pk=1)
        self.assertEqual(bid.getPrice(), 4)

    def test_bidFailBelowCurrentPrice(self):
        bidder = Bidder.objects.get(pk=1)
        item = Item.objects.get(pk=1)
        bid = Bid(_bidder=bidder, _bidPrice=1, _item=item)
        self.assertRaises(ValidationError, bid.save)

    def test_bidFailBelowMinIncrement(self):
        item = Item.objects.get(pk=1)
        bidder = Bidder.objects.get(pk=1)
        price = item.getPrice()
        increment = item.getMinIncrement()
        bid = Bid(_bidder=bidder, _bidPrice=price+increment-1, _item=item)
        self.assertRaises(ValidationError, bid.save)

    def test_bidCanBeMinimum(self):
        item = Item.objects.get(pk=2)
        bidder = Bidder.objects.get(pk=1)
        price = item.getPrice()
        bid = Bid(_bidder=bidder, _bidPrice=price, _item=item)
        bid.save()

    def test_cantBidBefore(self):
        auction = Auction(_name='tooearly', _passphrase='bidnotbegin',
                          _startTime=make_aware(datetime(2020, 5, 20, 0, 0, 0)),
                          _endTime=make_aware(datetime(2020, 5, 22, 0, 0, 0)))
        auction.save()
        item = Item(_auction=auction, _currentPrice=12, _name='leaf',
                     _description='it fell from a tree')
        item.save()
        bidder = Bidder.objects.get(pk=1)
        bid = Bid(_bidder=bidder, _item=item, _bidPrice=14)
        self.assertRaises(ValidationError, bid.save)

    def test_cantBidAfter(self):
        auction = Auction(_name='tooearly', _passphrase='bidnotbegin',
                          _startTime=make_aware(datetime(2020, 3, 20, 0, 0, 0)),
                          _endTime=make_aware(datetime(2020, 3, 22, 0, 0, 0)))
        auction.save()
        item = Item(_auction=auction, _currentPrice=12, _name='leaf',
                    _description='it fell from a tree')
        item.save()
        bidder = Bidder.objects.get(pk=1)
        bid = Bid(_bidder=bidder, _item=item, _bidPrice=14)
        self.assertRaises(ValidationError, bid.save)

class ImageTestCase(TestCase):
    '''
    Attributes:
        _image: Imagefield
        _item: Item instance

    Methods:
        getImage: ImageField
    '''
    def setUp(self):
        auction = Auction(_name='default auction', _passphrase='defaultauctionpassphrase',
                          _startTime=make_aware(datetime(2020, 3, 20, 0, 0, 0)),
                          _endTime=make_aware(datetime(2020, 3, 22, 0, 0, 0)))
        auction.save()

        item = Item(_auction=auction, _minIncrement=2, _currentPrice=2, _name='cow',
                    _description='it has utters', _isLive=False)
        item.save()

        item2 = Item(_auction=auction, _minIncrement=2, _currentPrice=2, _name='pig',
                    _description='it has ... fat?', _isLive=False)
        item2.save()

        image = Image(_item=item)
        image._image.save('test', File(open('alphaAuction/auction/static/auction/testImgs/test0_0.jpg', 'rb')))
        image.save()
    
        image2 = Image(_item=item)
        image2._image.save('test', File(open('alphaAuction/auction/static/auction/testImgs/test0_1.jpg', 'rb')))
        image2.save()

    def test_imageLocation(self):
        image = Image.objects.get(pk=1)
        self.assertEqual(image.getImage().url, '/media/test')

        image2 = Image.objects.get(pk=2)
        self.assertEqual(image.getImage().url, '/media/test') #this may look weird, but it's how django serves up files

