from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, Ruta
from django import template

class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['nombre_completo', 'correo_institucional', 'password1', 'password2', 'telefono', 'facultad', 'tipo_usuario']

    def clean_correo_institucional(self):
        correo = self.cleaned_data['correo_institucional']
        if not correo.endswith('@puce.edu.ec'):
            raise forms.ValidationError('El correo debe ser institucional (@puce.edu.ec)')
        return correo

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['correo_institucional']
        if commit:
            user.save()
        return user
    
class RutaForm(forms.ModelForm):
    class Meta: 
        model = Ruta
        fields = ['origen', 'fecha', 'hora_salida', 'asientos_disponibles', 'sitio_llegada']
    
        

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Correo institucional')
