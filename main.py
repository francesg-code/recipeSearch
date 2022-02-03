import requests
from dietary_requirements import options

# Please add 'app_id' and 'add_key' credentials from your Edamam account:
# https://developer.edamam.com/edamam-recipe-api
app_id = ''
app_key = ''
choices = []


def recipe_search(url):
    """Makes the API request to Edamam, checks to see if there are results and either asks the user to search again
    or returns the recipe results if successful."""
    result = requests.get(url)
    data = result.json()
    if data['hits'] == []:
        print('Sorry, no recipes found.')
        search_again()
    else:
        print('Recipes found!')
        return data['hits']


def create_file(ingredient, choices, results):
    """Saves the recipes to a file"""
    file_name = f'{ingredient}_recipes.txt'
    with open(f'{file_name}', 'w+') as text_file:
        text_file.write('Stop staring at the fridge!' + '\n')
        text_file.write(f'Recipe ingredient: {ingredient}' + '\n')
        for item in choices:
            text_file.write('Dietary requirement: ' + item + '\n')
        for result in results:
            recipe = result['recipe']
            text_file.write('\n')
            text_file.write(recipe['label'] + '\n')
            text_file.write(recipe['url'] + '\n')
        print(f'Recipes saved to {file_name}')


def search_again():
    """Allows the user to search again or exit. Clears previous selections."""
    search_again_choice = input('Would you like to search for another recipe? yes/no ')
    if search_again_choice.lower() == 'yes':
        choices.clear()
        recipe_search_is_on()
    else:
        print('Enjoy your meal! 😋')
        exit()


def recipe_search_is_on():
    """Adds user's choice of ingredient and dietary requirements to the API request url."""
    print('Stop staring at the fridge! 👀👀')
    ingredient = input('Please enter one ingredient: ')
    url = f'https://api.edamam.com/search?q={ingredient}&app_id={app_id}&app_key={app_key}'
    any_requirements = True
    while any_requirements:
        any_requirements_choice = input('Do you have any dietary requirements? yes/no: ')
        if any_requirements_choice.lower() == 'yes':
            any_requirements = False
            search_requirement = True
        elif any_requirements_choice.lower() == 'no':
            print(f'No dietary requirements chosen. Searching for recipes containing {ingredient} ... ')
            any_requirements = False
            search_requirement = False
        else:
            print("Please type \'yes\' or \'no\': ")

    while search_requirement:
        choice = input('Please type a dietary requirement or \'options\' to see the choices available, '
                       'or type \'done\' to search for a recipe: ')
        if choice.lower() == 'done':
            search_requirement = False
        elif choice.lower() == 'options':
            for key, value in options.items():
                print('Dietary requirement:', key, '\n', 'Description:', value)
        elif choice.lower() != 'done':
            for option in options:
                if choice == option:
                    url += f'&health={choice}'
                    choices.append(choice)
                    if len(choices) == 1:
                        print(f'The chosen dietary requirement is {choices}.')
                    else:
                        print(f'The chosen dietary requirements are {choices}.')

    results = recipe_search(url)

    for result in results:
        recipe = result['recipe']
        print(recipe['label'])
        print(recipe['url'])
        print()

    save_to_file = input('Would you like to save to file? yes/no: ')
    if save_to_file.lower() == 'yes':
        create_file(ingredient, choices, results)
    search_again()


recipe_search_is_on()
