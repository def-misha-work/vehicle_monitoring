from django import forms
from cars.models import TimePeriod, PlanPeriod


class TimePeriodForm(forms.ModelForm):
    shift1_start_hour = forms.IntegerField(
        min_value=0,
        max_value=23,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Начало смены 1 (часы)"
    )
    shift1_end_hour = forms.IntegerField(
        min_value=0,
        max_value=23,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Окончание смены 1 (часы)"
    )
    shift2_start_hour = forms.IntegerField(
        min_value=0,
        max_value=23,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Начало смены 2 (часы)"
    )
    shift2_end_hour = forms.IntegerField(
        min_value=0,
        max_value=23,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Окончание смены 2 (часы)"
    )
    shift3_start_hour = forms.IntegerField(
        min_value=0,
        max_value=23,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Начало смены 3 (часы)"
    )
    shift3_end_hour = forms.IntegerField(
        min_value=0,
        max_value=23,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Окончание смены 3 (часы)"
    )

    class Meta:
        model = TimePeriod
        fields = [
            'shift1_start', 'shift1_end',
            'shift2_start', 'shift2_end',
            'shift3_start', 'shift3_end',
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Преобразуем часы в формат времени
        instance.shift1_start = f"{self.cleaned_data['shift1_start_hour']:02d}:00"
        instance.shift1_end = f"{self.cleaned_data['shift1_end_hour']:02d}:00"
        instance.shift2_start = f"{self.cleaned_data['shift2_start_hour']:02d}:00"
        instance.shift2_end = f"{self.cleaned_data['shift2_end_hour']:02d}:00"
        instance.shift3_start = f"{self.cleaned_data['shift3_start_hour']:02d}:00"
        instance.shift4_end = f"{self.cleaned_data['shift3_end_hour']:02d}:00"
        if commit:
            instance.save()
        return instance


class PlanPeriodForm(forms.ModelForm):
    class Meta:
        model = PlanPeriod
        fields = ["plan_reisov", "plan_ves_za_period"]
        widgets = {
            "plan_reisov": forms.NumberInput(attrs={'type': 'number'}),
            "plan_ves_za_period": forms.NumberInput(attrs={'type': 'number'}),
        }
