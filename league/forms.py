from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class KayitFormu(UserCreationForm):
    # TODO: Hata mesajlarını türkçeleştir.
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label = "Kullanıcı Adı"
        self.fields["password1"].label = "Şifre"
        self.fields["password2"].label = "Şifre Doğrulama"

        self.fields['username'].help_text = (
            "Gereksinimler:\n"
            "Kullanıcı adınız 150 ya da daha az karakterden oluşmalı,\n"
            "Sadece harfler, rakamlar ve @/./+/-/_ işaretlerine izin verilir. "
        )
        
        self.fields['password1'].help_text = (
            "Gereksinimler:\n"
            "Parolanız en az 8 karakter içermeli,\n"
            "Parolanız sadece rakamlardan oluşamaz,\n"
            "Parolanız kullanıcı adınızla aynı olamaz."
        )

        self.fields['password2'].help_text = (
            "Doğrulama için lütfen aynı şifreyi giriniz."
        )

    class Meta:
        model = User
        fields = ("username",)