import sys
sys.path.append('/Users/epup/Private/Coding/Python/Flet/.venv/lib/python3.12/site-packages')
import deepl


auth_key = '65523bc2-d6ba-426e-b605-6646a6d1bc2c'
auth_key2 = "0847f781-6790-4fcd-8e84-e3ae6afd057d:fx"
translator = deepl.Translator(auth_key)

source_languages = {x.name: x.code for x in translator.get_source_languages()}
target_languages = {x.name: x.code for x in translator.get_target_languages()}

# print(target_languages)
# {'Bulgarian': 'BG', 'Czech': 'CS', 'Danish': 'DA', 'German': 'DE', 'Greek': 'EL', 'English (British)': 'EN-GB', 'English (American)': 'EN-US', 'Spanish': 'ES', 'Estonian': 'ET', 'Finnish': 'FI', 'French': 'FR', 'Hungarian': 'HU', 'Indonesian': 'ID', 'Italian': 'IT', 'Japanese': 'JA', 'Korean': 'KO', 'Lithuanian': 'LT', 'Latvian': 'LV', 'Norwegian': 'NB', 'Dutch': 'NL', 'Polish': 'PL', 'Portuguese (Brazilian)': 'PT-BR', 'Portuguese (European)': 'PT-PT', 'Romanian': 'RO', 'Russian': 'RU', 'Slovak': 'SK', 'Slovenian': 'SL', 'Swedish': 'SV', 'Turkish': 'TR', 'Ukrainian': 'UK', 'Chinese (simplified)': 'ZH-HANS'}

