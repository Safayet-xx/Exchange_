from django.contrib import admin
from django.utils.html import format_html
from .models import CreditWallet, CreditTransaction


@admin.register(CreditWallet)
class CreditWalletAdmin(admin.ModelAdmin):
    """Credit wallet management"""
    list_display = ['user_email', 'balance_display']
    search_fields = ['user__email']
    readonly_fields = ['user']
    ordering = ['-balance']
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User'
    
    def balance_display(self, obj):
        color = 'green' if obj.balance >= 5 else 'red'
        return format_html(
            '<strong style="color: {};">{} credits</strong>',
            color,
            obj.balance
        )
    balance_display.short_description = 'Balance'


@admin.register(CreditTransaction)
class CreditTransactionAdmin(admin.ModelAdmin):
    """Credit transaction management"""
    list_display = ['id', 'from_user_email', 'to_user_email', 'amount_display', 'note_display', 'created_at']
    list_filter = ['created_at']
    search_fields = ['from_user__email', 'to_user__email', 'note']
    readonly_fields = ['from_user', 'to_user', 'amount', 'note', 'session', 'created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Transaction', {
            'fields': ('from_user', 'to_user', 'amount')
        }),
        ('Details', {
            'fields': ('note', 'session', 'created_at')
        }),
    )
    
    def from_user_email(self, obj):
        return obj.from_user.email if obj.from_user else 'System'
    from_user_email.short_description = 'From'
    
    def to_user_email(self, obj):
        return obj.to_user.email if obj.to_user else 'System'
    to_user_email.short_description = 'To'
    
    def amount_display(self, obj):
        return format_html(
            '<strong style="color: blue;">{} credits</strong>',
            obj.amount
        )
    amount_display.short_description = 'Amount'
    
    def note_display(self, obj):
        return obj.note[:50] if obj.note else '-'
    note_display.short_description = 'Note'
    
    def has_add_permission(self, request):
        return False  # Transactions created through system only
    
    def has_change_permission(self, request, obj=None):
        return False  # Can't edit transactions
