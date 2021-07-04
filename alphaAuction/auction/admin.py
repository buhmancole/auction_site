from django.contrib import admin
from django.utils.html import format_html_join, format_html
from django.utils.safestring import mark_safe

# Register your models here.
from auction.models import Auction, Image

from auction.models import Bidder, Bid, Item

class ItemAdmin(admin.ModelAdmin):
    list_display = ('_name', '_currentPrice', '_auction', 'getWinner', '_isLive')
    list_filter = ('_auction', '_isLive', '_currentPrice')
    readonly_fields = ('current_winner', )

    def current_winner(self, instance):
        return f'{instance.getWinner()}'

class AuctionAdmin(admin.ModelAdmin):
    list_display = ('_name','_startTime','_endTime', '_passphrase' , 'getItems' )
    readonly_fields = ('earningsReport','winningBiddersReport')

    def winningBiddersReport(self, instance):
        return format_html_join(
                mark_safe('<br>'),
                '{} (#{}):<ol>{}<strong>Total Owed: ${}</strong></ol>',
                ((bidder.getFullName(), bidder.id, format_html_join(
                    '\n',
                    '<li>{} - ${}</li>',
                    ((item.getName(), item.getPrice()) for item in bidder.getItemsWinning())
                    ), bidder.getAmountOwed()) for bidder in instance.getWinners())
                )




    # short_description functions like a model field's verbose_name
    winningBiddersReport.short_description = "Report of Winning Bidders"

    def earningsReport(self, instance):
        return f'${instance.getEarnings()}'

    earningsReport.short_description = "Total Earnings"

class BidderAdmin(admin.ModelAdmin):
    list_display = ('getFirstName','getLastName', 'getEmail','getAmountOwed')
    readonly_fields = ('_favorites', '_auctions')

admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bidder, BidderAdmin)
admin.site.register(Bid)
admin.site.register(Item, ItemAdmin)
admin.site.register(Image)
