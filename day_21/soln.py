from itertools import chain
from copy import copy

class RecipeList():
    def __init__(self, in_file):
        self.recipes = [Recipe(line.strip()) for line in in_file.readlines()]
        self.allergens = set(chain.from_iterable(x.allergens for x in self.recipes))

        self.red_rec = copy(self.recipes)
        self.red_alg = copy(self.allergens)

        self.allergen_assign = dict()

        self.assign_allergens()

    def get_poss_ing(self, allergen):
        """ get all ingredients which are listed on all recipes 
            where 'allergen' is listed in the recipe's allergen list
        """
        cand_recs = [x.ingredients for x in self.red_rec if allergen in x.allergens]
        return list(set.intersection(*[set(i) for i in cand_recs]))
    
    def assign_allergens(self):
        """ recursively assign ingredients to allergens until no more definite 
            assignments can be made
        """
        ing_remove, alg_remove = set(), set()
        
        for a in self.red_alg:
            poss_ing = self.get_poss_ing(a)
            if len(poss_ing) == 1:
                alg_remove.add(a)
                ing_remove.add(poss_ing[0])
                self.allergen_assign[a] = poss_ing[0]
        
        if len(alg_remove) == 0 and len(ing_remove) == 0: # no movement since last call
            return 

        for rec in self.red_rec:
            rec.remove_ings(ing_remove)
            rec.remove_algs(alg_remove)
        self.red_alg = {x for x in self.red_alg if x not in alg_remove}

        if len(self.red_alg) == 0:
            return
        else:
            self.assign_allergens()

    def count_safe_ings(self):
        return sum(len(rec.ingredients) for rec in self.red_rec)

    def get_dangerous_ing_list(self):
        ings = sorted(self.allergen_assign.items(), key = lambda x: x[0])
        return ','.join(x[1] for x in ings)

class Recipe():
    def __init__(self, rec_line):
        ing, alg = self.parse(rec_line.strip())
        self.allergens = alg
        self.ingredients = ing 
    
    @staticmethod
    def parse(line):
        line = line.replace('(','').replace(')','')
        ing, alg = line.split(' contains ')
        ing = set(ing.split(' '))
        alg = set(alg.split(', '))
        return ing, alg
    
    def remove_ings(self, ings):
        self.ingredients = {x for x in self.ingredients if x not in ings}
    
    def remove_algs(self, algs):
        self.allergens = {x for x in self.allergens if x not in algs}

def p1(recipes):
    return recipes.count_safe_ings()

def p2(recipes):
    return recipes.get_dangerous_ing_list()


if __name__ == '__main__':
    # with open('input_test_1.txt') as my_file:
    with open('input.txt') as my_file:
        recipes = RecipeList(my_file)

    print(f'P1 Answer: {p1(recipes)}')
    print(f'P2 Answer: {p2(recipes)}')