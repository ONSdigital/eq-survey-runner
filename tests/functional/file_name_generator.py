import glob, os

for file in os.listdir(f'{os.curdir}/generated_pages/census_household_gb_wls'):
    if 'page.js' in file:
        file_names_parts = file.replace('.page.js', '').split('-')
        name = ''
        for part in file_names_parts:
            name += part.capitalize()

        print(
            f'const {name} = require(\'../../generated_pages/census_household_gb_wls/{file}\');'
        )
