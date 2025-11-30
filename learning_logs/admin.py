from django.contrib import admin

# Register your models here.
from learning_logs.models import Topic, Entry
class TopicAdmin(admin.ModelAdmin):
    list_display = ('text', 'owner', 'date_added')
    list_filter = ('owner', 'date_added')
    search_fields = ['text']

# === 2. Tùy chỉnh hiển thị Entry ===
class EntryAdmin(admin.ModelAdmin):
    # Hiển thị topic và chỉ một phần của text trên trang danh sách
    list_display = ('topic', 'display_text', 'date_added')
    list_filter = ('topic', 'date_added')
    search_fields = ['text']

    # Tạo một phương thức để hiển thị một đoạn ngắn của Entry text
    def display_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    display_text.short_description = 'Content Preview'

# === 3. Đăng ký các Model ===
admin.site.register(Topic, TopicAdmin)
admin.site.register(Entry, EntryAdmin)
