from django import forms
from cars.models import SmenaOne, PlanPeriod


class PlanPeriodForm(forms.ModelForm):
    class Meta:
        model = PlanPeriod
        fields = ["plan_reisov", "plan_ves_za_period"]
        widgets = {
            "plan_reisov": forms.TextInput(attrs={'type': 'text'}),
            "plan_ves_za_period": forms.TextInput(attrs={'type': 'text'}),
        }

        def clean_plan_reisov(self):
            data = self.cleaned_data['plan_reisov']
            if not data.isdigit():
                raise forms.ValidationError("Введите корректное число.")
            return int(data)

        def clean_plan_ves_za_period(self):
            data = self.cleaned_data['plan_ves_za_period']
            if not data.isdigit():
                raise forms.ValidationError("Введите корректное число.")
            return int(data)


class SmenaOneForm(forms.ModelForm):
    start = forms.IntegerField(
        min_value=0,
        max_value=24,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Начало смены (часы)"
    )
    end = forms.IntegerField(
        min_value=0,
        max_value=24,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Окончание смены (часы)"
    )

    class Meta:
        model = SmenaOne
        fields = ['start', 'end']
