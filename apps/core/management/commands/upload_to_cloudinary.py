import os
import cloudinary.uploader
from django.core.management.base import BaseCommand
from django.conf import settings
from pathlib import Path
from decouple import config

class Command(BaseCommand):
    help = 'Upload local media files to Cloudinary and remove them'

    def handle(self, *args, **options):
        # Configure Cloudinary
        cloudinary.config(
            cloud_name=config('CLOUDINARY_CLOUD_NAME'),
            api_key=config('CLOUDINARY_API_KEY'),
            api_secret=config('CLOUDINARY_API_SECRET')
        )

        base_dir = Path(settings.BASE_DIR)
        media_dir = base_dir / 'media'
        uploads_dir = base_dir / 'static' / 'uploads'
        signupimgs_dir = base_dir / 'static' / 'signupimgs'
        img_dir = base_dir / 'static' / 'img'

        dirs_to_upload = [media_dir, uploads_dir, signupimgs_dir, img_dir]

        for directory in dirs_to_upload:
            if directory.exists():
                for file_path in directory.rglob('*'):
                    if file_path.is_file():
                        try:
                            # Upload to Cloudinary
                            result = cloudinary.uploader.upload(str(file_path))
                            self.stdout.write(self.style.SUCCESS(f'Uploaded {file_path} to {result["url"]}'))
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f'Failed to upload {file_path}: {e}'))

        # Remove the directories
        for directory in dirs_to_upload:
            if directory.exists():
                import shutil
                shutil.rmtree(directory)
                self.stdout.write(self.style.SUCCESS(f'Removed directory {directory}'))