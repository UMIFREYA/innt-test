from django.contrib import admin
from .models import XToken, NFT, Wallet, IOS, Studio, TokenBalance, NFTBalance, StudioTransaction, Influence, IncentiveProof, Sorter

admin.site.register(XToken)
admin.site.register(NFT)
admin.site.register(Wallet)
admin.site.register(IOS)
admin.site.register(Studio)
admin.site.register(TokenBalance)
admin.site.register(NFTBalance)
admin.site.register(StudioTransaction)
admin.site.register(Influence)
admin.site.register(IncentiveProof)
admin.site.register(Sorter)
