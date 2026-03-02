from decimal import Decimal
import hashlib
import json 
import unicodedata

class Canonicalizer:
    @staticmethod
    def canonicalize(object: dict) -> str:

        #type coercision, unicode normalization, floats rouded
        for key, value in object.items():
            if isinstance(value, str):
                object[key] = unicodedata.normalize('NFD', value)
            elif isinstance(value, (float, Decimal)):
                object[key] = round(float(value), 4)
            elif isinstance(value, int):
                object[key] = float(value)
        
        #canonicalize one json dict, lexicographic ordering, keys sorted
        object = json.dumps(object, sort_keys=True, separators=(',', ':'))
        
        canonicalized_object = object.encode('utf-8')

        canonicalized_object = hashlib.sha256(canonicalized_object).hexdigest()

        return canonicalized_object


        
