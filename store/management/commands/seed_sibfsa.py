from django.core.management.base import BaseCommand
from store.models import Category, Product, ProductImage

class Command(BaseCommand):
    help = "Seed Sibfsa categories and flagship products"
    def handle(self, *args, **options):
        cat_oil, _ = Category.objects.get_or_create(slug='apricot_oil', defaults={'name':'Apricot Oil'})
        cat_serum, _ = Category.objects.get_or_create(slug='face_serum', defaults={'name':'Face Serum'})
        cat_shil, _ = Category.objects.get_or_create(slug='shilajit', defaults={'name':'Shilajit'})

        p1, _ = Product.objects.get_or_create(
            slug='apricot-oil-100ml',
            defaults=dict(
                name='Apricot Oil (100ml)',
                description='Cold-pressed apricot kernel oil from Gilgit-Baltistan. Pure, lightweight hydration for face, hair, and body. Batch-tested, amber glass.',
                price_pkr=2950, stock=100, is_featured=True, attributes={"size":"100ml","origin":"Gilgit-Baltistan","process":"Cold-pressed"}, category=cat_oil
            )
        )
        p2, _ = Product.objects.get_or_create(
            slug='apricot-oil-face-serum-30ml',
            defaults=dict(
                name='Apricot Oil Face Serum (30ml)',
                description='Glow + hydration serum with apricot kernel oil, rosehip, squalane, and vitamin E. Fragrance-free, lightweight, ritual-ready.',
                price_pkr=3950, stock=100, is_featured=True, attributes={"size":"30ml","blend":["Apricot","Rosehip","Squalane","Vitamin E"]}, category=cat_serum
            )
        )
        p3, _ = Product.objects.get_or_create(
            slug='pure-shilajit-20g',
            defaults=dict(
                name='Pure Shilajit (20g)',
                description='Lab-tested Himalayan/Karakoram shilajit resin. Batch COA available. Traditionally used to support daily vitality.',
                price_pkr=12500, stock=50, is_featured=True, attributes={"size":"20g","tests":["Heavy metals","Microbial"]}, category=cat_shil
            )
        )

        def ensure_img(prod, url, alt, pos=0):
            ProductImage.objects.get_or_create(product=prod, url=url, position=pos, defaults={'alt':alt})

        ensure_img(p1, 'https://images.unsplash.com/photo-1629196959209-1f24497d5ee9?auto=format&fit=crop&w=800&q=80', 'Apricot oil bottle on stone', 0)
        ensure_img(p1, 'https://images.unsplash.com/photo-1596461404969-9ae70c43b3aa?auto=format&fit=crop&w=800&q=80', 'Apricot kernels and oil texture', 1)
        ensure_img(p2, 'https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?auto=format&fit=crop&w=800&q=80', 'Face serum bottle with apricot', 0)
        ensure_img(p3, 'https://images.unsplash.com/photo-1541643600914-78b084683601?auto=format&fit=crop&w=800&q=80', 'Pure shilajit jar on slate', 0)

        self.stdout.write(self.style.SUCCESS('Seed complete: flagship products ready.'))