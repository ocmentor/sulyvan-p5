# -*- PipEnv -*-
# -*- coding: Utf-8 -*-

import records as rec

from Config.constants import *
from Database.database_user import DataBaseUser


class Main:
    """
        This class has the responsibility of directing the user
    """

    def __init__(self):
        """ Connect to Mysql database from the class DataBaseUser() """
        self.favorites = []
        self.db = self.connect_mysql()
        self.database = DataBaseUser(self.db)


    def home_menu(self):
        """ This function allows to direct the user """
        print('\n', DECO, '\n', "*** Bonjour et bienvenue au ° Substitute Factory ° ***", '\n', DECO, '\n')
        print("tapez:", '\n',
              " |-'1': Quel aliment souhaitez-vous remplacer ?" '\n',
              " |-'2': Retrouver mes aliments substitués" '\n',
              " |-'Q' pour Quitter", '\n')
        user = input()
        key_list = ["1", "2", "Q"]
        if user not in key_list:
            print('\n', "IndexError - |*** /!\ Tapez le chiffre associé à votre choix dans la liste /!\ ***|", '\n')
            self.home_menu()
        else:
            if user == '1':
                self.choice_category()
            elif user == '2':
                pass
                # self.database.get_favorites(user)
            if user == 'Q':
                quit()

    def choice_category(self):
        """ Choice Category """
        select_category = self.value_error(self.choice_category_action)
        print('\n', "|*** vous avez choisis ***| : ", select_category.capitalize(), '\n')
        self.choice_product(select_category)

    def choice_category_action(self):
        """ This function is linked with choice_category to control the user input """
        for i, get in enumerate(CATEGORIES):
            print("*", i+1, get)
        user = input('\n' " |*** Pour choisir une catégorie, tapez le chiffre associé et appuyer sur ENTREE ***| " '\n')
        return CATEGORIES[int(user) - 1]

    def choice_product(self, select_category):
        """ Choice product """
        select_product = self.value_error(self.choice_product_action, select_category)
        print('\n', "|*** vvous avez choisi ***| : ", select_product['name_product'].capitalize(), '\n')
        self.choice_substitute(select_category, select_product)

    def choice_product_action(self, select_category):
        """ This function is linked with choice_product to control the user input """
        products = self.database.get_all_products_per_category(str(select_category))
        for i, select in enumerate(products):
            print(f"* ({i+1}, {select['name_product']})")
        user = input('\n' " |*** Pour choisir un produit, tapez le chiffre associé et appuyer sur ENTREE ***| " '\n')
        if '0' in user:
            raise IndexError()
        return products[int(user) - 1]

    def choice_substitute(self, select_category, select_product):
        """ Choice the substitute """
        select_substitute = self.value_error(self.choice_substitute_action, select_category, select_product)
        self.choose_favorite_final(select_category, select_product, select_substitute)

    def choice_substitute_action(self, select_category, select_product):
        """ This function is linked with choice_substitute to control the user input """
        substitutes = self.database.choose_products_from_the_category(select_category, select_product)
        print("     | Code barre |,    | Nom Produits |,    | NutriScore |", '\n')
        for i, select in enumerate(substitutes):
            print(f"* ({i + 1}, {select['barcode']}, {select['name_product']}, {select['grade']})")
        user = input('\n' " | Vous pouvez choisir un produits" '\n'
                     " |-tapez le chiffre associé et appuyer sur ENTREE" '\n'
                     " |-'Q' pour Quitter" '\n'
                     " |-'H' retour au Menu" '\n')
        if user.isdigit():
            select_substitute = substitutes[int(user)]
            print('\n', "Vous avez choisi : ", select_substitute, '\n', '\n',
                  "|*** Souhaitez-vous sauvegarder ce produit ? ***|", '\n')
            self.choose_favorite_final(select_category, select_product, select_substitute)
        else:
            key_list = ["C", "H", "Q"]
            if user not in key_list:
                self.choice_substitute_action(select_category, select_product)
            elif user == 'C':
                self.choice_substitute_action(select_category, select_product)
            elif user == 'H':
                self.home_menu()
            elif user == 'Q':
                quit()
        return substitutes[int(user) - 1]


    def choose_favorite_final(self, select_category, select_product, select_substitute):
        """ Choose de products final substitue and save in the data base """
        user = input(" | tapez:" '\n' 
                     " |-'O': pour Oui" '\n'
                     " |-'N': pour Non" '\n' 
                     " |-'C': pour Choisir un nouveau produit" '\n' 
                     " |-'H': retour au Menu" '\n'
                     " |-'Q': pour Quitter, valider avec ENTREE" '\n')
        if user.isdigit():
            print('\n', "IndexError - |*** /!\ Veuillez faire un choix parmi la liste /!\ ***|", '\n')
            self.choose_favorite_final(select_category, select_product, select_substitute)
        else:
            key_list = ["O", "N", "C", "H", "Q"]
            if user not in key_list:
                print('\n', "ValueError - |*** /!\ Tapez le chiffre associé à votre choix dans la liste /!\ ***|", '\n')
                self.choose_favorite_final(select_category, select_product, select_substitute)
            elif user == 'O':
                self.favorites.extend(select_substitute)
                print('\n', " |*** Ajout du produit :", select_substitute, "successful ***|", '\n')
                self.choice_substitute_action(select_category, select_product)
            elif user == 'N':
                self.choice_substitute_action(select_category, select_product)
            elif user == 'C':
                self.choice_substitute_action(select_category, select_product)
            elif user == 'H':
                self.home_menu()
            elif user == 'Q':
                quit()

    def value_error(self, select_function, *args):
        """ This function will control the user's input """
        try:
            return select_function(*args)
        except ValueError:
            print('\n', "ValueError - |*** /!\ Tapez le chiffre associé à votre choix dans la liste /!\ ***|", '\n')
            return self.value_error(select_function, *args)
        except IndexError:
            print('\n', "IndexError - |*** /!\ Tapez le chiffre associé à votre choix dans la liste /!\ ***|", '\n')
            return self.value_error(select_function, *args)

    def connect_mysql(self):
        """ Connecting in the database """
        self.db = rec.Database(f"mysql+mysqlconnector://{USER}:{PASSWORD}@localhost/"
                               f"{DATABASE}?charset=utf8mb4")
        return self.db

def main():
    """ Initialize the main class """

    init = Main()
    init.home_menu()


if __name__ == "__main__":
    main()
