from django.forms import BooleanField, CheckboxInput, ModelForm

from mailing.models import Client, Message, MailingSettings


class StyleFormMixin:
    """Миксин для стилизации формы"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            elif not isinstance(field, CheckboxInput):
                field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, ModelForm):
    """Форма для добавления нового клиента и редактирования"""
    class Meta:
        model = Client
        fields = '__all__'


class MessageForm(StyleFormMixin, ModelForm):
    """Форма для добавления нового сообщения и редактирования"""
    class Meta:
        model = Message
        fields = '__all__'


class MailingSettingsForm(StyleFormMixin, ModelForm):
    """Форма для добавления новой рассылки и редактирования"""
    class Meta:
        model = MailingSettings
        exclude = ('mailing_status', )
