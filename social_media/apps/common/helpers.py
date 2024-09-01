import hashlib
import uuid
import datetime
import random

from rest_framework import serializers


def generate_auth_token():
    unique_id = str(uuid.uuid4())
    key = hashlib.sha256((unique_id + datetime.datetime.now().isoformat() + str(random.random())).encode('utf-8'))
    return key.hexdigest()


def common_serializer(meta_model=None, meta_fields=[]):
    meta_fields = [*meta_fields]
    class _serializer(serializers.ModelSerializer):
        class Meta:
            model = meta_model
            fields = meta_fields
    return _serializer
