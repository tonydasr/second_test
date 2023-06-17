import datetime
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserChangeForm

class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']


class AccountDetailsForm(forms.ModelForm):
    class Meta:
        model = AccountDetails
        fields = ['gender', 'birth_date', 'picture']


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ['street_address', 'city', 'postal_code', 'country']

class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "contact_no",
        ]


class AccountDetailsForm(forms.ModelForm):

    class Meta:
        model = AccountDetails
        fields = [

            'gender',
 
            
        ]


class UserAddressForm(forms.ModelForm):
    COUNTRY_CHOICES = [
        ('', 'Select Country'),
        ('AF', 'Afghanistan'),
        ('AL', 'Albania'),
        ('AM', 'Armenia'),
        ('AO', 'Angola'),
        ('AR', 'Argentina'),
        ('AT', 'Austria'),
        ('AZ', 'Azerbaijan'),
        ('BA', 'Bosnia and Herzegovina'),
        ('BB', 'Barbados'),
        ('BD', 'Bangladesh'),
        ('BE', 'Belgium'),
        ('BF', 'Burkina Faso'),
        ('BG', 'Bulgaria'),
        ('BH', 'Bahrain'),
        ('BI', 'Burundi'),
        ('BJ', 'Benin'),
        ('BO', 'Bolivia'),
        ('BR', 'Brazil'),
        ('BS', 'Bahamas'),
        ('BT', 'Bhutan'),
        ('BW', 'Botswana'),
        ('BY', 'Belarus'),
        ('BZ', 'Belize'),
        ('CA', 'Canada'),
        ('CF', 'Central African Republic'),
        ('CH', 'Switzerland'),
        ('CL', 'Chile'),
        ('CM', 'Cameroon'),
        ('CN', 'China'),
        ('CO', 'Colombia'),
        ('CR', 'Costa Rica'),
        ('CU', 'Cuba'),
        ('CV', 'Cape Verde'),
        ('CY', 'Cyprus'),
        ('CZ', 'Czech Republic'),
        ('DE', 'Germany'),
        ('DJ', 'Djibouti'),
        ('DM', 'Dominica'),
        ('DO', 'Dominican Republic'),
        ('DZ', 'Algeria'),
        ('EC', 'Ecuador'),
        ('EE', 'Estonia'),
        ('EG', 'Egypt'),
        ('ER', 'Eritrea'),
        ('ES', 'Spain'),
        ('ET', 'Ethiopia'),
        ('FI', 'Finland'),
        ('FR', 'France'),
        ('GA', 'Gabon'),
        ('GB', 'United Kingdom'),
        ('GD', 'Grenada'),
        ('GE', 'Georgia'),
        ('GH', 'Ghana'),
        ('GM', 'Gambia'),
        ('GN', 'Guinea'),
        ('GR', 'Greece'),
        ('GT', 'Guatemala'),
        ('GW', 'Guinea-Bissau'),
        ('GY', 'Guyana'),
        ('HN', 'Honduras'),
        ('HR', 'Croatia'),
        ('HT', 'Haiti'),
        ('HU', 'Hungary'),
        ('ID', 'Indonesia'),
        ('IE', 'Ireland'),
        ('IL', 'Israel'),
        ('IN', 'India'),
        ('IQ', 'Iraq'),
        ('IR', 'Iran'),
        ('IS', 'Iceland'),
        ('IT', 'Italy'),
        ('JM', 'Jamaica'),
        ('JO', 'Jordan'),
        ('JP', 'Japan'),
        ('KE', 'Kenya'),
        ('KG', 'Kyrgyzstan'),
        ('KH', 'Cambodia'),
        ('KM', 'Comoros'),
        ('KN', 'Saint Kitts and Nevis'),
        ('KP', 'North Korea'),
        ('KR', 'South Korea'),
        ('KW', 'Kuwait'),
        ('KZ', 'Kazakhstan'),
        ('LA', 'Laos'),
        ('LB', 'Lebanon'),
        ('LC', 'Saint Lucia'),
        ('LI', 'Liechtenstein'),
        ('LK', 'Sri Lanka'),
        ('LR', 'Liberia'),
        ('LS', 'Lesotho'),
        ('LT', 'Lithuania'),
        ('LU', 'Luxembourg'),
        ('LV', 'Latvia'),
        ('LY', 'Libya'),
        ('MA', 'Morocco'),
        ('MD', 'Moldova'),
        ('ME', 'Montenegro'),
        ('MG', 'Madagascar'),
        ('MK', 'Macedonia'),
        ('ML', 'Mali'),
        ('MM', 'Myanmar'),
        ('MN', 'Mongolia'),
        ('MR', 'Mauritania'),
        ('MU', 'Mauritius'),
        ('MV', 'Maldives'),
        ('MW', 'Malawi'),
        ('MX', 'Mexico'),
        ('MY', 'Malaysia'),
        ('MZ', 'Mozambique'),
        ('NA', 'Namibia'),
        ('NE', 'Niger'),
        ('NG', 'Nigeria'),
        ('NI', 'Nicaragua'),
        ('NL', 'Netherlands'),
        ('NO', 'Norway'),
        ('NP', 'Nepal'),
        ('OM', 'Oman'),
        ('PA', 'Panama'),
        ('PE', 'Peru'),
        ('PG', 'Papua New Guinea'),
        ('PH', 'Philippines'),
        ('PK', 'Pakistan'),
        ('PL', 'Poland'),
        ('PS', 'Palestinian Territory'),
        ('PT', 'Portugal'),
        ('PY', 'Paraguay'),
        ('QA', 'Qatar'),
        ('RO', 'Romania'),
        ('RS', 'Serbia'),
        ('RU', 'Russia'),
        ('RW', 'Rwanda'),
        ('SA', 'Saudi Arabia'),
        ('SB', 'Solomon Islands'),
        ('SC', 'Seychelles'),
        ('SD', 'Sudan'),
        ('SE', 'Sweden'),
        ('SG', 'Singapore'),
        ('SI', 'Slovenia'),
        ('SK', 'Slovakia'),
        ('SL', 'Sierra Leone'),
        ('SM', 'San Marino'),
        ('SN', 'Senegal'),
        ('SO', 'Somalia'),
        ('SR', 'Suriname'),
        ('SS', 'South Sudan'),
        ('SV', 'El Salvador'),
        ('SY', 'Syria'),
        ('SZ', 'Swaziland'),
        ('TD', 'Chad'),
        ('TG', 'Togo'),
        ('TH', 'Thailand'),
        ('TJ', 'Tajikistan'),
        ('TL', 'East Timor'),
        ('TM', 'Turkmenistan'),
        ('TN', 'Tunisia'),
        ('TO', 'Tonga'),
        ('TR', 'Turkey'),
        ('TT', 'Trinidad and Tobago'),
        ('TW', 'Taiwan'),
        ('TZ', 'Tanzania'),
        ('UA', 'Ukraine'),
        ('UG', 'Uganda'),
        ('US', 'United States'),
        ('UY', 'Uruguay'),
        ('UZ', 'Uzbekistan'),
        ('VC', 'Saint Vincent and the Grenadines'),
        ('VE', 'Venezuela'),
        ('VN', 'Vietnam'),
        ('VU', 'Vanuatu'),
        ('WS', 'Samoa'),
        ('YE', 'Yemen'),
        ('ZA', 'South Africa'),
        ('ZM', 'Zambia'),
        ('ZW', 'Zimbabwe')
    ]
    country = forms.ChoiceField(choices=COUNTRY_CHOICES, label='Country', widget=forms.Select(attrs={'class': 'form-control'}))


    class Meta:
        model = UserAddress
        fields = [

            'postal_code',
            'country'
        ]






class UserLoginForm(forms.Form):
    username = forms.CharField(label="Username/Email")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Invalid login credentials")
            if not user.is_active:
                raise forms.ValidationError("This account is inactive.")

        return super(UserLoginForm, self).clean(*args, **kwargs)



class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ['schema_id', 'invest_amount', 'wallet']
