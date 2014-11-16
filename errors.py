

#               API Errors codes               #


INVALID_INPUT_VALUE = {
    'code': 101,
    'msg' : {
        'fr' : "Valeur(s) saisie(s) incorrecte(s).",
        'en' : "Invalid input(s) value(s)."
    }
}

INVALID_COORDS_VALUE = {
    'code': 102,
    'msg' : {
        'fr' : "Valeur(s) de coordonnée(s) incorrecte(s).",
        'en' : "Invalid coords value(s)."
    }
}

TOO_MOO_SHORT_TIME = {
    'code': 103,
    'msg' : {
        'fr' : "Trop de Meuh envoyés en un temps trop court.",
        'en' : "Too many Moos in a too short time."
    }
}

INVALID_KEY = {
    'code': 201,
    'msg' : {
        'fr' : "Cette clé d'API est incorrecte.",
        'en' : "This API key is invalid."
    }
}

BLACKLISTED_KEY = {
    'code': 202,
    'msg' : {
        'fr' : "Cette clé d'API est blacklistée.",
        'en' : "This API key is blacklisted."
    }
}

INVALID_ID = {
    'code': 104,
    'msg' : {
        'fr' : "Cet identifiant n'est pas valide.",
        'en' : "This ID is invalid."
    }
}

INVALID_USERNAME = {
    'code': 105,
    'msg' : {
        'fr' : "Ce nom d'utilisateur n'existe pas ou n'est pas associé à cette clé d'API.",
        'en' : "This username doesn't exist or is not associated to this key."
    }
}

ALREADY_EXISTING_USERNAME = {
    'code': 106,
    'msg' : {
        'fr' : "Ce nom d'utilisateur existe déjà. Merci d'en sélectionner un nouveau.",
        'en' : "This username already exists. Please choose a new one."
    }
}



import json
from django.http import HttpResponseBadRequest, JsonResponse
from django.utils.translation import get_language
from womoobox.settings import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES


# Default format for a success api call
def format_success(add_infos):
    full_infos = {'result' : 'succeed' }
    full_infos.update(add_infos)
    response = JsonResponse(full_infos) # dict for json
    response['Access-Control-Allow-Origin'] = "*"
    return response


# Format error to return information by json
def format_error(error):
    # select language
    language = get_language()
    if language not in SUPPORTED_LANGUAGES:
        language = DEFAULT_LANGUAGE
    # build error message
    full_error = {
        'error_code': error['code'],
        'error_message': (error['msg'][language])
    }
    response = HttpResponseBadRequest(json.dumps(full_error),
                                      content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response