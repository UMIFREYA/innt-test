from .models import XToken, NFT, Wallet, Studio,TokenBalance, NFTBalance,StudioTransaction,Influence,IncentiveProof,Sorter
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import XToken, NFT, Wallet, Studio,TokenBalance, NFTBalance,StudioTransaction,Influence,IncentiveProof,Sorter
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseForbidden


def transfer_token(sender_wallet, receiver_wallet, token, amount):
    # 检查发送方余额是否足够
    sender_token_balance = get_object_or_404(TokenBalance, wallet=sender_wallet, x_token=token)
    if sender_token_balance.balance < amount:
        return False

    # 检查接收方是否存在对应的TokenBalance
    receiver_token_balance, _ = TokenBalance.objects.get_or_create(wallet=receiver_wallet, x_token=token)

    # 调整余额
    sender_token_balance.balance -= amount
    sender_token_balance.save()
    receiver_token_balance.balance += amount
    receiver_token_balance.save()
    
    return True


def transfer_studio_token(sender_wallet_id, receiver_wallet_id, token_id, amount, reason, asset_name=None):
    sender_wallet = get_object_or_404(Wallet, pk=sender_wallet_id)
    receiver_wallet = get_object_or_404(Wallet, pk=receiver_wallet_id)
    token = get_object_or_404(XToken, pk=token_id)

    success = transfer_token(sender_wallet, receiver_wallet, token, amount)

    if success:
        receiver_token_balance, _ = TokenBalance.objects.get_or_create(wallet=receiver_wallet, x_token=token)

        transaction = StudioTransaction.objects.create(
            sender_wallet=sender_wallet,
            receiver_wallet=receiver_wallet,
            token=token,
            amount=amount,
            reason=reason
        )
        transaction.save()

        if reason == 'Purchasing Asset':
            nft = NFT.objects.create(name=asset_name, description='Purchase Asset:'+asset_name)
            NFTBalance.objects.create(wallet=sender_wallet, nft=nft)

        message = 'Success'
    else:
        message = 'Balance Limit'

    return success, message



from decimal import Decimal

def update_project_rating(studio, a_token_amount, grade):
    new_size = studio.assessment_size + a_token_amount
    new_rating = (studio.current_rating * studio.assessment_size + a_token_amount * grade) / new_size
    studio.assessment_size = new_size
    studio.current_rating = new_rating
    studio.save()

def update_sorter_assessment_size(sorter, a_token_amount):
    sorter.assessment_size += a_token_amount
    sorter.save()

def create_incentive_proof(user, a_token_amount, grade, sorter,studio):
    contribution_factor = Decimal(a_token_amount) / (Decimal(sorter.assessment_size) / Decimal(Studio.objects.count()))
    incentive_proof = IncentiveProof.objects.create(contribution_factor=contribution_factor, grade=grade, user=user,studio=studio)
    incentive_proof.save()


def create_studio_function(name, description, creator):
    Studio.objects.create(name=name, description=description, creator=creator)

def upgrade_to_IOS_function(studio, ios_version):
    # 获取名为projectF的 agent wallet
    projectf_agent_wallet = Wallet.objects.get(name='projectF', type='AGENT')

    token = XToken.objects.create(name=studio.name, total_supply=1000)
    if ios_version == 'IOS X1':
        studio_wallet_balance = 100
        agent_wallet_balance = 900
    elif ios_version == 'IOS X2':
        studio_wallet_balance = 200
        agent_wallet_balance = 800
    else:
        studio_wallet_balance = 300
        agent_wallet_balance = 700

    # 创建新的 studio wallet
    studio_wallet = Wallet.objects.create(type='STUDIO', name=studio.name, owner=studio.creator)

    studio.IOS_kernel = ios_version
    studio.studio_wallet = studio_wallet
    studio.agent_wallet = projectf_agent_wallet
    studio.is_active = True
    studio.save()

    TokenBalance.objects.create(wallet=studio_wallet, x_token=token, balance=studio_wallet_balance)
    TokenBalance.objects.create(wallet=projectf_agent_wallet, x_token=token, balance=agent_wallet_balance)

