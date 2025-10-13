from rest_framework import serializers
import re


class EmailSerializerValidator:

    def validate_email(self, email):
        email_reg = r'...+@..+\...+'
        if email and not re.fullmatch(email_reg, email):
            raise serializers.ValidationError("Указан не верный формат почты.")
        return email
    

class PhoneSerializerValidator:
    
    def validate_phone(self, phone):
        phone_reg = r'(?:\+7|8)(?:\s|\()\d{3}(?:\s|\))\s?\d{3}(?:\s|-)\d{2}(?:\s|-)\d{2}'
        if phone and not re.fullmatch(phone_reg, phone):
            raise serializers.ValidationError("Указан не верный формат телефона.")
        return phone