from django.core.management.base import BaseCommand, CommandError
from app.models import *
import traceback
import json

class Command(BaseCommand):
    help = 'Create data'
    def handle(self, *args, **kwargs):
        try:
            json_path = f"./assets/static/json/countries.json"
            json_file = open(json_path, "r")
            json_data = json.load(json_file)
            for data in json_data:
                if not Country_Code.objects.filter(name=data["name"]).exists():
                    Country_Code.objects.create(name=data["name"],short_name=data["code"],dial_code=data['dial_code'],flag=data['flag'])
        except:
            traceback.print_exc()