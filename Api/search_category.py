# -*- PipEnv -*-
# -*- coding: Utf-8 -*-

# https://fr.openfoodfacts.org/api/v0/produit/'barre_code'.json


import requests as req
from pprint import pprint

from Config.constants import *


class ApiCollectingData:
    """ Call the Api Open Food Fact """

    def __init__(self):
        """ The constructor is not used here """

    def bring_out(self):
        """ Use the configuration for the connecting interface """
        all_products = []
        barre_code = ''
        pl = "cgi/search.pl"
        api = "https://fr.openfoodfacts.org/" + pl                         # Address OpenFooFact.org the API FR locating
        bc_search = api + "api/v0/produit/" + barre_code + ".json"                    # Address only barre_code research
        for category in CATEGORIES:
            config = {"action": "process",                                         # This config for  for connecting API
                      "tagtype_0": "categories",                                            # Get the result by category
                      'tag_0': category,                                         # the tag represents the article search
                      "tag_contains_0": "contains",
                      "page_size": 5,                                                   # Number of articles per page
                      "json": 1}                                                              # The API response in JSON

            response = req.get(api, params=config)                           # Uses the configuration for the connection
            results = response.json()                                                      # Return the response in JSON
            products_section = results['products']                                               # Finally result of API

            for product in products_section:
                product['main_category'] = category                             # Convert the categories -> sub_category
            all_products.extend(products_section)

        ###############################
        """ PRINT RESULTS FUNCTION """
        ###############################
        """ Pprint the first result the API response """
        # pprint(all_products)

        """##########################"""

        return all_products

    def validate_the_data(self, keys, products_section):
        """ Validate the complete fields """
        for key in keys:
            if key not in products_section or not products_section[key]:
                return False
        return True

    def format_final_response(self, all_products):
        """ Formatted the response just harvest the categories selected """
        product_final = []
        keys = ['id', 'product_name_fr', 'nutrition_grade_fr', 'url', 'categories', 'main_category', 'stores']
        print(len(all_products))
        for product in all_products:
            if self.validate_the_data(keys, product):

                barre_code = product['id']
                name = product['product_name_fr']
                grade = product['nutrition_grade_fr']
                website = product['url']
                categories = product['categories'].upper().split(',')
                sub_category = product['main_category'].upper()
                stores = product['stores'].upper().split(',')
                # Respect of the order of the criteria insert in a tuple and simple format in database insert
                key = (barre_code, name, grade, website, categories, sub_category,  stores)
                formatting = key
                product_final.append(formatting)

                ###############################
                """ PRINT RESULTS FUNCTION """
                ###############################
                """ Print type results the stores and category count """
                print('produit: ', name.upper())
                print('disponnible dans', [len(stores)], 'magasin(s): = ', stores)
                print('présent dans', [sub_category], [len(categories)], 'categorie(s): = ', categories, '\n')
                """ Pprint final result the API response formatted """
                # pprint(product_final)
                print(f"Nous avons récupéré {len(product_final)} produits")

                """##########################"""

        return product_final


def main():
    # Download the response

    downloader = ApiCollectingData()
    connect = downloader.bring_out()
    final = downloader.format_final_response(connect)

    # Save the response in file

    # save_date = save.save_data(final, 'Response_save.csv')


if __name__ == "__main__":
    main()
