from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import XToken, NFT, Wallet, Studio,TokenBalance, NFTBalance,StudioTransaction,Influence,IncentiveProof,Sorter
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseForbidden

from .function_views import transfer_token,transfer_studio_token,update_project_rating,update_sorter_assessment_size,create_incentive_proof


from .forms import  TransferStudioTokenForm
import markdown

## 底层的测试页面部分


from .function_views import create_studio_function
@login_required
def create_studio(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        creator = request.user
        create_studio_function(name, description, creator)
        return redirect('home')
    else:
        return render(request, 'create_studio.html')





from .function_views import upgrade_to_IOS_function
@login_required
def upgrade_to_IOS(request, pk):
    studio = get_object_or_404(Studio, pk=pk)
    if request.method == 'POST':
        try:
            ios_version = request.POST['ios_version']
        except MultiValueDictKeyError:
            return render(request, 'upgrade_to_IOS.html', {'studio': studio, 'error_message': 'IOS version not selected'})

        upgrade_to_IOS_function(studio, ios_version)
        return redirect('studio_manage', pk=studio.pk)
    else:
        return render(request, 'upgrade_to_IOS.html', {'studio': studio})



@login_required
def studio_wallet_manage(request, pk):
    studio = get_object_or_404(Studio, pk=pk)
    studio_wallet = studio.studio_wallet
    token_balances = TokenBalance.objects.filter(wallet=studio_wallet)
    NFT_balances = NFTBalance.objects.filter(wallet=studio_wallet)

    

    if request.method == 'POST':
        form = TransferStudioTokenForm(request.POST, studio_wallet_id=studio_wallet.id)
        if form.is_valid():
            sender_wallet_id = studio_wallet.id
            receiver_wallet_id = form.cleaned_data['receiver_wallet'].id
            token_id = form.cleaned_data['token'].id
            amount = form.cleaned_data['amount']
            reason = form.cleaned_data['reason']
            asset_name = form.cleaned_data.get('asset_name', None)

            success, message = transfer_studio_token(sender_wallet_id, receiver_wallet_id, token_id, amount, reason, asset_name)
            messages.add_message(request, messages.INFO, message)
            return redirect('studio_wallet_manage', pk=studio.pk)

    else:
        form = TransferStudioTokenForm(studio_wallet_id=studio_wallet.id)

    return render(request, 'studio_wallet_manage.html', {'studio': studio, 'token_balances': token_balances,'NFT_balances': NFT_balances, 'form': form})



@login_required
def rate_studio(request, studio_id):
    if request.method == 'POST':
        user = request.user
        studio = get_object_or_404(Studio, pk=studio_id)
        # 这里保留rate_studio中现有的代码
        grade = int(request.POST['grade'])
        a_token_amount = int(request.POST['a_token_amount'])

        # 获取名为projectA的agent wallet
        projecta_agent_wallet = Wallet.objects.get(name='projectA', type='AGENT')
        # 获取用户的Influence
        user_influence, _ = Influence.objects.get_or_create(user=user)
        # 获取用户的private wallet
        user_private_wallet = Wallet.objects.get(owner=user, type='PRIVATE')

        # 检查用户private wallet中的A token数量是否足够
        a_token = XToken.objects.get(name='A token')  # 假设平台只有一种A token
        user_a_token_balance = get_object_or_404(TokenBalance, wallet=user_private_wallet, x_token=a_token)
        if user_a_token_balance.balance < a_token_amount:
            return render(request, 'rate_studio.html', {'studio': studio, 'error_message': 'Insufficient A token balance'})

        # 进行评分
        success, message = transfer_studio_token(user_private_wallet.id, projecta_agent_wallet.id, a_token.id, a_token_amount, 'Rating')

        if success:
            # 更新项目评分
            update_project_rating(studio, a_token_amount, grade)

            # 更新排序器的Assessment size
            sorter = Sorter.objects.first()  # 假设平台只有一个排序器
            update_sorter_assessment_size(sorter, a_token_amount)

            # 生成Incentive proof
            create_incentive_proof(user, a_token_amount, grade, sorter,studio)

        # ...
        
        # 重定向到rate_studio_page
        return redirect('rate_studio_page', studio_id=studio_id)
    else:
        # 如果不是POST请求，重定向到rate_studio_page
        return redirect('rate_studio_page', studio_id=studio_id)


@login_required
def rate_studio_page(request, studio_id):
    studio = get_object_or_404(Studio, pk=studio_id)
    studio_wallet = studio.studio_wallet
    NFTs = NFTBalance.objects.filter(wallet=studio_wallet)
    tokens = TokenBalance.objects.filter(wallet=studio_wallet)
    user_private_wallet = Wallet.objects.get(owner=request.user, type='PRIVATE')
    a_token = XToken.objects.get(name='A token')
    user_a_token_balance = get_object_or_404(TokenBalance, wallet=user_private_wallet, x_token=a_token)
    return render(request, 'rate_studio.html', {'studio': studio, 'user_a_token_balance': user_a_token_balance,'NFTs':NFTs,'tokens':tokens})




    
#-----只查不写的部分--------


def personal_page(request, user_id):
    user = request.user
    influence = Influence.objects.get(user=user)
    token_balances = TokenBalance.objects.filter(wallet__owner=user, wallet__type=Wallet.PRIVATE)
    incentive_proofs = IncentiveProof.objects.filter(user=user)

    context = {
        'user': user,
        'influence': influence,
        'token_balances': token_balances,
        'incentive_proofs': incentive_proofs,
    }

    return render(request, 'personal_page.html', context)






@login_required
def studio_index(request):
    studios = Studio.objects.filter(creator=request.user)
    active_studios = studios.filter(is_active=True)
    inactive_studios = studios.filter(is_active=False)
    return render(request, 'studio_index.html', {'active_studios': active_studios, 'inactive_studios': inactive_studios})


@login_required
def studio_manage(request, pk):
    studio = get_object_or_404(Studio, pk=pk)
    if request.user != studio.creator:
        return HttpResponseForbidden("You don't have permission to access this page.")
    return render(request, 'studio_manage.html', {'studio': studio})


#名义上的首页
def landing(request):
    return render(request, 'landing.html')

#控制页面
def home(request):
    return render(request, 'home.html')


#Creator页面
def creator_view(request):
    return render(request, 'creator_view.html')

#player页面
def player_view(request):
    return render(request, 'player_view.html')

def studio_overview(request):
    studios = Studio.objects.all()

    return render(request, 'studio_overview.html', {'studios':studios})





#-----管理器会用到的部分--------

def initialize_sorter(request):
    # 1. 清除所有排序器相关参数
    Influence.objects.all().delete()
    TokenBalance.objects.filter(x_token__name='A token').delete()
    XToken.objects.filter(name='A token').delete()
    Wallet.objects.filter(name='projectA', type='AGENT').delete()
    Sorter.objects.all().delete()


    # 2. 将所有用户的影响力设置为200；创建名为A token的X token
    a_token = XToken.objects.create(name='A token', total_supply=0)

    for user in User.objects.all():
        influence = Influence.objects.create(user=user, score=200)
        # 3. 根据影响力数据，向所有用户的私人钱包发送等量的A token
        private_wallet, created = Wallet.objects.get_or_create(type='PRIVATE', owner=user)
        TokenBalance.objects.create(wallet=private_wallet, x_token=a_token, balance=influence.score)

        # 更新A token的总供应量
        a_token.total_supply += influence.score
    a_token.save()

    # 4. 创建名为projectA的agent wallet
    Wallet.objects.create(name='projectA', type='AGENT')


    # 5. 排序器初始量
    Sorter.objects.create(assessment_size=200)
    
    return redirect('home')


@login_required
def initialize(request):
    # 创建名为projectF的agent wallet
    projectf_agent_wallet = Wallet.objects.create(type='AGENT', name='projectF')
    projectf_agent_wallet = Wallet.objects.create(type='AGENT', name='projectA')


    # 创建K token，total supply = 100000
    k_token = XToken.objects.create(name='K Token', total_supply=100000)

    # 为projectF增加100,000的K token余额
    TokenBalance.objects.create(wallet=projectf_agent_wallet, x_token=k_token, balance=100000)

    return redirect('home')




@login_required
def clear_data(request):
    # 删除所有的 Studio
    Studio.objects.all().delete()

    # 删除所有的 Wallet
    Wallet.objects.all().delete()

    # 删除所有的 XToken
    XToken.objects.all().delete()

    # 删除所有的 NFT
    NFT.objects.all().delete()

    # 删除所有的 NFTBalance
    NFTBalance.objects.all().delete()

    IncentiveProof.objects.all().delete()

    # 返回首页
    return redirect('home')







    

#------基本不会修改的部分--------

from django.contrib.auth import logout

def user_logout(request):
    logout(request)
    return redirect('home')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, '登录成功！')
            return redirect('home')
        else:
            messages.error(request, '用户名或密码错误！')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            # 创建私人钱包
            Wallet.objects.create(type='PRIVATE',name = username, owner=user)
            
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

