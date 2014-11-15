# Configuration


# generate key with specific length and chars
import string
KEY_LENGTH = 50 
KEY_REF_SETS = string.ascii_letters + string.digits

# when getting last moos to init map
MAX_NUMBER_OF_INITIAL_MOO = 25
# when getting last moos from last call
MAX_NUMBER_OF_MOO = 25
# do not accept more than 1 (same animal) moo every X minutes
MIN_DURATION_BETWEEN_MOO = 1 # minutes

# supported languages
SUPPORTED_LANGUAGES = (
    'fr',
    'en',
)
DEFAULT_LANGUAGE = SUPPORTED_LANGUAGES[1]