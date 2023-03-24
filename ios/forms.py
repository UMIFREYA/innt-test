from django import forms
from .models import Wallet, XToken,TokenBalance

class TransferStudioTokenForm(forms.Form):
    receiver_wallet = forms.ModelChoiceField(queryset=Wallet.objects.none(), label='接收方钱包')
    token = forms.ModelChoiceField(queryset=XToken.objects.none(), label='代币类型')
    amount = forms.IntegerField(min_value=1, label='数量')
    REASON_CHOICES = [
        ('Fundraising', 'Fundraising'),
        ('Expense', 'Expense'),
        ('Purchasing Asset', 'Purchasing Asset'),
        ('Reason4', 'Reason4'),
    ]
    reason = forms.ChoiceField(choices=REASON_CHOICES, label='原因')
    asset_name = forms.CharField(required=False, label='资产名称')

    def __init__(self, *args, **kwargs):
        studio_wallet_id = kwargs.pop('studio_wallet_id')
        super(TransferStudioTokenForm, self).__init__(*args, **kwargs)
        studio_wallet_token_ids = TokenBalance.objects.filter(wallet__id=studio_wallet_id).values_list('x_token_id', flat=True)
        self.fields['token'].queryset = XToken.objects.filter(id__in=studio_wallet_token_ids)
        self.fields['receiver_wallet'].queryset = Wallet.objects.exclude(id=studio_wallet_id)


    def clean(self):
        cleaned_data = super().clean()
        reason = cleaned_data.get('reason')
        asset_name = cleaned_data.get('asset_name')

        if reason == 'Purchasing Asset' and not asset_name:
            self.add_error('asset_name', '请输入资产名称')
