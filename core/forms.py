from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, Ruta
from django import template

class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['nombre_completo', 'correo_institucional', 'password1', 'password2', 'telefono', 'facultad', 'tipo_usuario']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar mensajes en español
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        
        # Personalizar etiquetas
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'
        
        # Mensajes de error personalizados
        self.fields['password1'].error_messages = {
            'required': 'Este campo es obligatorio.',
        }
        self.fields['password2'].error_messages = {
            'required': 'Este campo es obligatorio.',
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

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
