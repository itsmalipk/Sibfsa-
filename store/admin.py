from django.contrib import admin
from .models import Category, Product, ProductImage, Review, Order, OrderItem


# ======================
# Category Admin
# ======================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")  # removed created_at
    search_fields = ("name",)
    ordering = ("name",)


# ======================
# Product Admin
# ======================
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "stock")  # removed price
    list_filter = ("category",)
    search_fields = ("name", "description")
    ordering = ("id",)
    inlines = [ProductImageInline]


# ======================
# Review Admin
# ======================
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "user", "rating")  # safe fields
    list_filter = ("rating",)
    search_fields = ("user__username", "product__name")
    ordering = ("-id",)


# ======================
# Order Admin
# ======================
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "status")  # removed user + total_price
    list_filter = ("status",)
    search_fields = ("id",)
    ordering = ("-id",)
    inlines = [OrderItemInline]


# ======================
# Order Item Admin
# ======================
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity")  # removed price
    search_fields = ("product__name", "order__id")
