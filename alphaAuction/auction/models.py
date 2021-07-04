from datetime import datetime
from django.utils.timezone import make_aware
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
import uuid
lettersOnly = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
PASSWORD_MAX_LENGTH = 20
PASSWORD_MIN_LENGTH = 8

class Auction(models.Model):
    _startTime = models.DateTimeField()
    _endTime = models.DateTimeField()
    _name = models.TextField(max_length=50)
    _passphrase = models.TextField(max_length=50, unique=True, validators=[lettersOnly])


    def __str__(self):
        return self._name

    def isRunning(self):
        return self._endTime > make_aware(datetime.now()) and self._startTime < make_aware(datetime.now())

    def getBidders(self):
        return self.bidder_set.all() 

    def containsBidder(self, bidder):
        return len(self.bidder_set.filter(id=bidder.id)) > 0

    def getStart(self):
        return self._startTime

    def changeStart(self, newStart):
        self._startTime = newStart
        try:
            self.full_clean()
            return True
        except Exception as e:
            return False

    def getEnd(self):
        return self._endTime

    def changeEnd(self, newEnd):
        self._endTime = newEnd
        return True

    def getItems(self):
        return self.item_set.all() 

    def getLiveItems(self):
        return self.item_set.filter(_isLive = True)

    def getSilentItems(self):
        return self.item_set.filter(_isLive = False)

    def changePass(self, newPass):
        self._passphrase = newPass
        try:
            self.full_clean()
            return True
        except Exception as e:
            return False

    def getPass(self):
        return self._passphrase

    def getName(self):
        return self._name

    def changeName(self, newName):
        self._name = newName
        return True

    def getEarnings(self):
        result = 0
        for item in self.getItems():
            result+=item.getWorth()
        return result

    def getWinners(self):
        winners= []
        ids = []
        for item in self.getItems():
            if item.getWorth() > 0:
                bidder = item.getWinner()
                try:
                    ids.index(bidder.id)
                except:
                    winners.append(bidder)
                    ids.append(bidder.id)
        return winners 
        
        
    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if self._startTime > self._endTime:
            raise ValidationError({"_endTime": _("Auction end time must be after start time.")})


    #force validation on save
    def save(self, *args, **kwargs):
            self.full_clean()
            super().save()




class Item(models.Model):
    def validate_positive(value):
        if value < 1 :
            raise ValidationError(_('%(value)s must be >= 1.'),params={'value':value},)

    _name = models.TextField(max_length=50)
    _description = models.TextField()
    _auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    _currentPrice = models.IntegerField(validators=[validate_positive])
    _minIncrement = models.IntegerField(default=1, validators=[validate_positive])
    _isLive = models.BooleanField(default=False)
    _Set_Winner_Bidder_Number = models.CharField(max_length=10, blank=True, null=True)
        
    class Categories(models.TextChoices):
        ANTIQUES = 'AQ', _('Antiques')
        BOOKS = 'BK', _('Books')
        EXPERIENCE = 'EX', _('Experience')
        FOOD = 'FD', _('Food')
        GIFT_BASKET = 'GB', _('Gift Basket')
        SCHOOL_SUPPLIES = 'SS', _('School Supplies')
        SPORTING_GOODS = 'SG', _('Sporting Goods')
        TOY = 'TY', _('Toy')
        TECHNOLOGY = 'TC', _('Technology')
        MISC = 'MC', _('Miscellaneous')

    _category = models.CharField(
        max_length=2,
        choices=Categories.choices,
    )

    def __str__(self):
        return self._name

    def getCategory(self):
        return self._category

    def changeCategory(self, new):
        self._category = new
        return True

    def getWinner(self):
        if self.getIsLive():
            if self._Set_Winner_Bidder_Number:
                return Bidder.objects.get(id=self._Set_Winner_Bidder_Number)
            else:
                return None
        #get the highest bid associated with this item, then return it's bidder
        bids = self.bid_set.all().order_by('-_bidPrice')
        if len(bids) > 0:
            return bids.first().getBidder()
        else:
            return None
     
    def getAuction(self):
        return self._auction

    def changeAuction(self, auction):
        self._auction = auction
        return True

    def changeDesc(self, new):
        self._description = new
        return True

    def changeMinIncrement(self, new):
        self._minIncrement = new
        try:
            self.full_clean()
            return True
        except:
            return False

    def changeIsLive(self, new):
        self._isLive = new
        return True

    def getIsLive(self):
        return self._isLive

    def getDesc(self):
        return self._description

    def changeName(self, new):
        self._name = new
        return True

    def getName(self):
        return self._name

    def getImages(self):
        return self.image_set.all()

    def getPrice(self):
        return self._currentPrice

    def getWorth(self):
        if self.getWinner() == None:
            return 0
        return self._currentPrice
    
    def changePrice(self, price):
        self._currentPrice = price
        try:
            self.full_clean()
            return True
        except:
            return False

    def getMinIncrement(self):
        if self.getWinner() == None:
            return 0
        return self._minIncrement

    def getBids(self):
        return self.bid_set.all()

    def save(self, *args, **kwargs):
        if self._category == '':
            self._category = Item.Categories.MISC
        self.full_clean()
        super().save()


#an image class to enable Items to have multiple images
class Image(models.Model):
    _image = models.ImageField()
    _item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def getImage(self):
        return self._image


class Bidder(AbstractUser):
    _auctions = models.ManyToManyField(Auction)
    _favorites = models.ManyToManyField(Item)
    _resetHash = models.TextField(blank=True,null=True)
    _columns = models.IntegerField(default=4)
    _currentAuction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='the_current_auction', null=True, blank=True)

    def __str__(self):
        return f'{self.getFullName()} (#{self.id})'

    def getCurrentAuction(self):
        return self._currentAuction

    def changeCurrentAuction(self, newAuction):
        self._currentAuction = newAuction
        self.save()
        return True

    def getColumns(self):
        return self._columns

    def changeColumns(self, col):
        self._columns = col
        return True

    def getFavorites(self):
        return self._favorites.all()

    def addFavorite(self, item):
        self._favorites.add(item)
        self.save()
        return True

    def removeFavorite(self, item):
        self._favorites.remove(item)
        self.save()
        return True

    def getCurrentFavorites(self):
        current = []
        currentItems = self._currentAuction.getItems()
        for favorite in self._favorites.all():
            if favorite in currentItems:
                current.append(favorite)
        return current

    def getFullName(self):
        return self.first_name+" "+self.last_name

    def getFirstName(self):
        return self.first_name

    def getLastName(self):
        return self.last_name

    def changeFirstName(self, new):
        self.first_name = new
        return True

    def changeLastName(self, new):
        self.last_name = new
        return True

    def addAuction(self, auction):
        if auction not in self._auctions.all():
            self._auctions.add(auction)
            self.save()
            return True
        return False

    def changePassword(self, new):
        try:
            if len(new) >= PASSWORD_MIN_LENGTH and len(new) <= PASSWORD_MAX_LENGTH and not self.check_password(new):
                self.set_password(new)
                self.save()
                self.full_clean()
                return True
            return False
        except Exception as e:
            #print(e)
            return False

    def getEmail(self):
        return self.email

    def changeEmail(self, new):
        try:
            self.email = new
            self.save()#throws an Integrity error if email isn't unique
            return True
        except Exception as e:
            #print(e)
            return False
            
    def getAuctions(self):
        return self._auctions.all()

    def getAmountOwed(self):
        total = 0
        for item in self.getItemsBidOn():
            if item.getWinner().id == self.id:
                total+=item.getPrice()
        return total

    def getItemsBidOn(self):
        items = []
        indexs = []
        for bid in self.bid_set.all():
            try:
                indexs.index(bid.getItem().id)
                continue
            except ValueError:
                items.append(bid.getItem())
                indexs.append(bid.getItem().id)
        return items

    def getItemsWinning(self):
        items = []
        indexs = []
        for bid in self.bid_set.all():
            try:
                if bid.getItem().getWinner().id == self.id:
                    indexs.index(bid.getItem().id)
                continue
            except ValueError:
                items.append(bid.getItem())
                indexs.append(bid.getItem().id)
        return items

    def save(self, *args, **kwargs):
        #ensure email is lowercase
        self.email = self.getEmail().lower()
        if not self.is_superuser:
            self.username = self.email
            self.full_clean()#calls the Email validator (and all others)
        else:
            self.email = self.username
            self.first_name = self.username
        super().save()

    def generateResetHash(self):
        hash = uuid.uuid4().hex
        self._resetHash = hash
        self.save()
        return hash

class Bid(models.Model):
    _bidPrice = models.IntegerField()
    _timestamp = models.DateTimeField(auto_now=True)
    _bidder = models.ForeignKey(Bidder, on_delete=models.CASCADE)
    _item = models.ForeignKey(Item, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return self._bidder.getFullName() +": $"+ str(self._bidPrice) +" on " + self.getItem().getName()

    def getBidder(self):
        return self._bidder

    def getItem(self):
        return self._item

    def getPrice(self):
        return self._bidPrice

    def getTime(self):
        return self._timestamp

    #add a couple special field validations
    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if self._bidPrice < self._item.getPrice()+ self._item.getMinIncrement():
            raise ValidationError({"_bidPrice": _(f"Bid must be higher than the item's current bid (${self._item.getPrice()}) by at least ${self._item.getMinIncrement()}.")})
        if not self.getItem().getAuction().isRunning():
            raise ValidationError({"Auction": _("The auction is not currently running.")})
        if self.getItem().getIsLive():
            raise ValidationERror({"Live Item":_("You cannot bid on a live item.")})

    #override save to ensure a valid bid on save
    def save(self, *args, **kwargs):
            self.full_clean()
            self._item.changePrice(self._bidPrice)
            self._item.save()
            super().save(*args, **kwargs) #call the 'real' save() method
    
