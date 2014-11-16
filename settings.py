# Configuration


# Generate key with specific length and chars
import string
KEY_LENGTH = 50 
KEY_REF_SETS = string.ascii_letters + string.digits

# When getting last Moos to init map
MAX_NUMBER_OF_INITIAL_MOO = 25
# When getting last Moos from last call
MAX_NUMBER_OF_MOO = 25
# Do not accept more than 1 (same animal) moo every X minutes
MIN_DURATION_BETWEEN_MOO = 1 # minutes

# Supported languages
SUPPORTED_LANGUAGES = (
    'fr',
    'en',
)
DEFAULT_LANGUAGE = SUPPORTED_LANGUAGES[1]