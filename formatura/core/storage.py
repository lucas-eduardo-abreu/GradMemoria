import cloudinary.uploader
import cloudinary.utils
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible


@deconstructible
class CloudinaryStorage(Storage):
    def _save(self, name, content):
        result = cloudinary.uploader.upload(
            content,
            public_id=name.rsplit('.', 1)[0],
            overwrite=True,
        )
        return result['public_id']

    def _open(self, name, mode='rb'):
        raise NotImplementedError("Cloudinary não suporta leitura direta de arquivos.")

    def exists(self, name):
        try:
            cloudinary.api.resource(name)
            return True
        except Exception:
            return False

    def url(self, name):
        url, _ = cloudinary.utils.cloudinary_url(name, fetch_format='auto', quality='auto')
        return url

    def delete(self, name):
        cloudinary.uploader.destroy(name)

    def get_available_name(self, name, max_length=None):
        return name
