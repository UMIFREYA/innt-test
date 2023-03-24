from django.db import models

class XToken(models.Model):
    name = models.CharField(max_length=255)  # token的名称
    total_supply = models.IntegerField()  # token的总量

class NFT(models.Model):
    name = models.CharField(max_length=255)  # NFT的名称
    description = models.TextField()  # NFT的介绍

class Wallet(models.Model):
    PRIVATE = 'PRIVATE'
    STUDIO = 'STUDIO'
    AGENT = 'AGENT'
    TYPE_CHOICES = [
        (PRIVATE, 'Private Wallet'),
        (STUDIO, 'Studio Wallet'),
        (AGENT, 'Agent Wallet'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)  # 钱包的类型
    name = models.CharField(max_length=255, null=True, blank=True)  # 钱包的名称，如果是Studio Wallet，则与对应的OS studio的名称相同
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)  # 钱包的控制者，如果是Agent Wallet，则为空

    
class IOS(models.Model):
    IOS_CHOICES = [
        ('IOS X1', 'IOS X1'),
        ('IOS X2', 'IOS X2'),
        ('IOS X3', 'IOS X3'),
        ('IOS N', 'IOS N')
    ]
    ios_choices = models.CharField(max_length=10,choices = IOS_CHOICES,default='IOS N')
    
class Studio(models.Model):
    name = models.CharField(max_length=255)  # studio的名称
    description = models.TextField()  # studio的介绍
    creator = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # studio的创建者
    is_active = models.BooleanField(default=False)  # studio是否激活

    # 当studio被激活时填充以下字段
    studio_wallet = models.OneToOneField(Wallet, on_delete=models.CASCADE, related_name='os_studio', null=True, blank=True)  # 对应的studio wallet
    agent_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='os_studios', null=True, blank=True)  # 对应的Agent Wallet
    IOS_kernel = models.CharField(max_length=10, choices=IOS.IOS_CHOICES, null=True, blank=True)  # IOS kernel版本
        
    
    # 评分
    assessment_size = models.IntegerField(default=0)  # 评分状态
    current_rating = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)  # 当前评分

    def update_rating(self, a_token_amount, grade):
        self.assessment_size += a_token_amount
        self.current_rating = (self.current_rating * (self.assessment_size - a_token_amount) + a_token_amount * grade) / self.assessment_size
        self.save()


 

class TokenBalance(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    x_token = models.ForeignKey(XToken, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)

    class Meta:
        unique_together = ('wallet', 'x_token')


class NFTBalance(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE)



from django.utils import timezone

class StudioTransaction(models.Model):
    REASON_CHOICES = [
        ('Fundraising', 'Fundraising'),
        ('Expense', 'Expense'),
        ('purchasing asset', 'purchasing asset'),
        ('Reason4', 'Reason4'),
    ]

    sender_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='sent_transactions')
    receiver_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='received_transactions')
    token = models.ForeignKey(XToken, on_delete=models.CASCADE)
    amount = models.IntegerField()
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)



class Influence(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    score = models.IntegerField(default=200)


class IncentiveProof(models.Model):
    contribution_factor = models.DecimalField(max_digits=5, decimal_places=4)
    grade = models.IntegerField(default=0)
    studio = models.ForeignKey(Studio,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

class Sorter(models.Model):
    name = models.CharField(max_length=255)
    assessment_size = models.IntegerField(default=0)