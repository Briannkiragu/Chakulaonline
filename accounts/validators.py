import os

from django.core.exceptions import ValidationError


def allow_only_images_validator(value):
    ext = os.path.splitext(value.name)[1].lower()  # .jpg, .png, .jpeg
    valid_extensions = ['.jpg', '.png', '.jpeg']
    if ext not in valid_extensions:
        raise ValidationError('Unsupported file extension. Allowed extensions: ' + str(valid_extensions))