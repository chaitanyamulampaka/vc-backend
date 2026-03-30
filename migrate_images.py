import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'varaha_backend.settings')
django.setup()

import cloudinary.uploader
from products.models import Product, ProductImage

def migrate_images():
    base_dir = settings.BASE_DIR
    media_dir = os.path.join(base_dir, 'media')

    # Migrate Product.img
    for product in Product.objects.exclude(img=''):
        img_field = product.img
        public_id = img_field.public_id
        # The local path is media_dir + public_id, but since public_id includes 'product_imgs/', and media_dir has product_imgs/, it's media/product_imgs/filename
        local_path = os.path.join(media_dir, public_id)
        if os.path.exists(local_path):
            try:
                result = cloudinary.uploader.upload(local_path, public_id=public_id, folder='')
                print(f"Uploaded {local_path} to Cloudinary")
            except Exception as e:
                print(f"Error uploading {local_path}: {e}")
        else:
            print(f"Local file not found: {local_path}")

    # Migrate ProductImage.image
    for pimg in ProductImage.objects.all():
        img_field = pimg.image
        public_id = img_field.public_id
        local_path = os.path.join(media_dir, public_id)
        if os.path.exists(local_path):
            try:
                result = cloudinary.uploader.upload(local_path, public_id=public_id, folder='')
                print(f"Uploaded {local_path} to Cloudinary")
            except Exception as e:
                print(f"Error uploading {local_path}: {e}")
        else:
            print(f"Local file not found: {local_path}")

if __name__ == '__main__':
    migrate_images()