from django import forms
from cars.models import TimePeriod, PlanPeriod


class TimePeriodForm(forms.ModelForm):
    class Meta:
        model = TimePeriod
        fields = ["start_time", "end_time"]
        widgets = {
            "start_time": forms.DateTimeInput(
                attrs={"type": "datetime-local"}
            ),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class PlanPeriodForm(forms.ModelForm):
    class Meta:
        model = PlanPeriod
        fields = ["plan_reisov", "plan_ves_za_period"]
        widgets = {
            "plan_reisov": forms.NumberInput(attrs={'type': 'number'}),
            "plan_ves_za_period": forms.NumberInput(attrs={'type': 'number'}),
        }
