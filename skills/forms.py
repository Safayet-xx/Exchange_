from django import forms
from .models import UserSkill, Skill, SkillCategory


class UserSkillForm(forms.ModelForm):
    # Use CharField instead of ModelChoiceField to allow 'other'
    skill = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'skill_select'}),
        required=False,
        label='Select Skill'
    )
    
    custom_skill_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter skill name',
            'id': 'custom_skill_name'
        }),
        label='Custom Skill Name'
    )
    
    class Meta:
        model = UserSkill
        fields = ['department', 'proficiency_level', 'years_of_experience', 'description']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'proficiency_level': forms.Select(attrs={'class': 'form-control'}),
            'years_of_experience': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': '0'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe your experience with this skill...'}),
        }
        labels = {
            'department': 'Department',
            'proficiency_level': 'Proficiency Level',
            'years_of_experience': 'Years of Experience',
            'description': 'Description (Optional)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Order skills alphabetically and add "Other" option
        skills = list(Skill.objects.all().order_by('name'))
        
        # Create choices with "Other" at the end
        choices = [('', '--- Select a skill ---')] + [(str(s.id), s.name) for s in skills] + [('other', '➕ Other (Add Custom Skill)')]
        self.fields['skill'].widget.choices = choices
        
        # If editing, set initial skill value
        if self.instance and self.instance.pk:
            self.fields['skill'].initial = str(self.instance.skill.id)
    
    def clean(self):
        cleaned_data = super().clean()
        skill_value = cleaned_data.get('skill')
        custom_skill_name = cleaned_data.get('custom_skill_name')
        
        # If "Other" selected, custom name is required
        if skill_value == 'other':
            if not custom_skill_name:
                raise forms.ValidationError('Please enter a custom skill name.')
            
            # Create or get the custom skill
            skill_obj, created = Skill.objects.get_or_create(
                name=custom_skill_name.strip(),
                defaults={'category': SkillCategory.objects.get_or_create(name='Other', defaults={'icon': '📌'})[0]}
            )
            cleaned_data['skill'] = skill_obj
        elif not skill_value:
            raise forms.ValidationError('Please select a skill or choose "Other" to add a custom skill.')
        else:
            # Convert string ID to Skill object
            try:
                skill_obj = Skill.objects.get(id=int(skill_value))
                cleaned_data['skill'] = skill_obj
            except (ValueError, Skill.DoesNotExist):
                raise forms.ValidationError('Invalid skill selected.')
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # The skill is already set in cleaned_data
        instance.skill = self.cleaned_data['skill']
        if commit:
            instance.save()
        return instance
