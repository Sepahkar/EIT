from django import forms
from HR.models import Users, ConstValue


class UsersForm(forms.ModelForm):
    qs_Degree_Type = ConstValue.objects.filter(
        Code__startswith="Degree", Parent__isnull=False
    )
    Degree_Type = forms.ModelChoiceField(
        queryset=qs_Degree_Type,
        label=ConstValue.objects.filter(Code__startswith="Degree", Parent__isnull=True)
        .first()
        .Caption,
    )

    class Meta:
        model = Users
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
