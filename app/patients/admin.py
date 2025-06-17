from django import forms
from django.contrib import admin
from .models import Patient


class MyAdminSite(admin.AdminSite):
    site_header = "Проект: Дендритные клетки"
    site_title = 'Дендритные клетки'
    index_title = 'Редактирование базы пациентов'


admin_site = MyAdminSite(name="myadmin")


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        widgets = {
            'note_txt': forms.Textarea(attrs={
                'rows': 20,
                'cols': 100,
                'class': 'large-textarea'
            }),
            'oper_txt': forms.Textarea(attrs={
                'rows': 10,
                'cols': 80
            }),
        }

class PatientAdmin(admin.ModelAdmin):
    form = PatientForm
    # Поля, отображаемые в таблице
    list_display = (
        'last_modified',
        'actual_date',
        'fio',
        'birthday',
        'sex',
        'cure_order',
        'last_contact_date',
        'statendyr',
        'prrecid_date',
        'datediag',
        'mkb10',
        'txtdiag',
        'stage',
        't',
        'n',
        'm',
        'g',
        'p16',
        'focus_size',
        'node_size',
        'note_txt',
        'oper_date',
        'oper_txt',
        'oper_complications',
        'dendritic',
        'kindlech_txt',
        'fk_after',
        'fk_last',
        'neut',
        'limph',
        'plt'
    )

    # Поля, доступные для редактирования в таблице
    list_editable = (
        'actual_date',
        'fio',
        'birthday',
        'sex',
        'cure_order',
        'last_contact_date',
        'statendyr',
        'prrecid_date',
        'datediag',
        'mkb10',
        'txtdiag',
        'stage',
        't',
        'n',
        'm',
        'g',
        'p16',
        'focus_size',
        'node_size',
        'note_txt',
        'oper_date',
        'oper_txt',
        'oper_complications',
        'dendritic',
        'kindlech_txt',
        'fk_after',
        'fk_last',
        'neut',
        'limph',
        'plt'
    )

    # Поиск по полям
    search_fields = (
        'last_modified',
        'actual_date',
        'fio',
        'birthday',
        'sex',
        'cure_order',
        'last_contact_date',
        'statendyr',
        'prrecid_date',
        'datediag',
        'mkb10',
        'txtdiag',
        'stage',
        't',
        'n',
        'm',
        'g',
        'p16',
        'focus_size',
        'node_size',
        'note_txt',
        'oper_date',
        'oper_txt',
        'oper_complications',
        'dendritic',
        'kindlech_txt',
        'fk_after',
        'fk_last',
        'neut',
        'limph',
        'plt'
    )

    # Фильтры справа
    list_filter = (
        'last_modified',
        'actual_date',
        'birthday',
        'sex',
        'cure_order',
        'last_contact_date',
        'statendyr',
        'prrecid_date',
        'datediag',
        'mkb10',
        'stage',
        't',
        'n',
        'm',
        'g',
        'p16',
        'focus_size',
        'node_size',
        'oper_date',
        'oper_complications',
        'dendritic',
        'kindlech_txt',
        'fk_after',
        'fk_last',
        'neut',
        'limph',
        'plt'
    )

    # Количество записей на странице
    list_per_page = 5

admin_site.register(Patient, PatientAdmin)