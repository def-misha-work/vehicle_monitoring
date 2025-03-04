from django import forms

from cars.models import PlanPeriod, SmenaOne, SmenaThree, SmenaTwo


class PlanPeriodForm(forms.ModelForm):
    class Meta:
        model = PlanPeriod
        fields = ["plan_reisov", "plan_ves_za_period"]
        widgets = {
            "plan_reisov": forms.TextInput(attrs={"type": "text"}),
            "plan_ves_za_period": forms.TextInput(attrs={"type": "text"}),
        }

        def clean_plan_reisov(self):
            data = self.cleaned_data["plan_reisov"]
            if not data.isdigit():
                raise forms.ValidationError("Введите корректное число.")
            return int(data)

        def clean_plan_ves_za_period(self):
            data = self.cleaned_data["plan_ves_za_period"]
            if not data.isdigit():
                raise forms.ValidationError("Введите корректное число.")
            return int(data)


class SmenaOneForm(forms.ModelForm):
    class Meta:
        model = SmenaOne
        fields = ["start", "end"]
        widgets = {
            "start": forms.NumberInput(attrs={"min": 0, "max": 23}),
            "end": forms.NumberInput(attrs={"min": 0, "max": 23}),
        }


class SmenaTwoForm(forms.ModelForm):
    class Meta:
        model = SmenaTwo
        fields = ["start", "end"]
        widgets = {
            "start": forms.NumberInput(attrs={"min": 0, "max": 23}),
            "end": forms.NumberInput(attrs={"min": 0, "max": 23}),
        }


class SmenaThreeForm(forms.ModelForm):
    class Meta:
        model = SmenaThree
        fields = ["start", "end"]
        widgets = {
            "start": forms.NumberInput(attrs={"min": 0, "max": 23}),
            "end": forms.NumberInput(attrs={"min": 0, "max": 23}),
        }
