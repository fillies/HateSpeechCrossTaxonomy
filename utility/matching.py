import pandas as pd
from pandas import DataFrame
import csv
from autocorrect import Speller

class Matcher:
    match_id = {'No-hate': 0, 'Hate': 1, 'Target_of_hate': 2, 'Class': 3, 'Working_class': 4,
                'Immigration_status': 5, 'Asylum_seeker': 6, 'Foreigner': 7, 'Immigrants': 8, 'Refugee': 9, 'Movement': 10, 'LGBTQ+': 11,
                'National_origin': 12, 'China': 13, 'Korea': 14, 'Pakistan': 15, 'Other_N': 16, 'Poland': 17,
                'Russian': 18, 'Physical_attributes': 19, 'Age': 20, 'Old': 21, 'Young': 22, 'Disability': 23,
                'Gender': 24, 'Gender_minorities': 25, 'Trans': 26, 'Man': 27, 'Women': 28, 'Overweight': 29,
                'Skin_color': 30, 'White': 31, 'Non_white': 32, 'Black': 33, 'Race_Ethnicity': 34, 'Arabs': 35,
                'Asia': 36, 'East_A': 37, 'South_A': 38, 'South_east': 39, 'Black_people': 40, 'Europe': 41,
                'East_E': 42, 'Hispanic': 43, 'Indigenous': 44, 'Aboriginal_people': 45, 'Minority_groups': 46, 'Mixed_race': 47,
                'People_from_Africa': 48, 'Travelers': 49, 'Roma': 50, 'Religion_or_belief': 51, 'Hindus': 52,
                'Jews': 53, 'Muslims': 54, 'Other_R': 55, 'Sexuality': 56, 'Bisexual': 57, 'Gay': 58, 'Lesbian': 59,
                'Types_of_hate': 60, 'Animosity': 61, 'Dehumanization': 62, 'Derogation': 63,
                'Support_for_hateful_entities': 64, 'Threatening_language': 65}

    first_level_groups = [('Target_of_hate', [3, 59]), ('Types_of_hate', [61, 66])]
    match_first_level_groups = {'Target_of_hate': 2, 'Types_of_hate': 60}

    secound_level_groups = [('Class', [4, 4]), ('Immigration_status', [6, 9]), ('Movement', [11, 11]),
                            ('National_origin', [13, 18]), ('Physical_attributes', [20, 33]),
                            ('Race_Ethnicity', [35, 50]), ('Religion_or_belief', [52, 55]), ('Sexuality', [57, 59])]
    match_secound_level_groups = {'Class': 3, 'Immigration_status': 5, 'Movement': 10, 'National_origin': 12,
                                  'Physical_attributes': 19, 'Race_Ethnicity': 34, 'Religion_or_belief': 51,
                                  'Sexuality': 56}

    third_level_groups = [('Age', [21, 22]), ('Gender', [25, 28]), ('Skin_color', [31, 33]), ('Asia', [37, 39]),
                          ('Europe', [42, 42]), ('Indigenous', [45, 45]), ('Travelers', [50, 50])]
    match_third_level_groups = {'Age': 20, 'Gender': 24, 'Skin_color': 30, 'Asia': 36, 'Europe': 41,
                                'Indigenous': 44,
                                'Travelers': 49}

    frouth_level_groups = [('Gender_minorities', [26, 26]), ('Non_white', [33, 33])]
    match_fourth_level_groups = {'Gender_minorities': 25, 'Non_white': 32}


    match_name = {'hate': 'hate', 'target': 'target_of_hate', 'cl': 'Class', 'wc': 'Working_class',
                  'is': 'Immigration_status', 'asylum': 'Asylum_seeker', 'for': 'Foreigner', 'immig': 'Immigrants',
                  'ref': 'Refugee', 'move': 'Movement', 'lgbtq': 'LGBTQ+', 'no': 'National_origin', 'chin': 'China',
                  'kore': 'Korea', 'pak': 'Pakistan', 'other_n': 'Other_N', 'pol': 'Poland', 'russian': 'Russian',
                  'pa': 'Physical_attributes', 'age': 'Age', 'dis': 'Disability', 'gen': 'Gender',
                  'gendermin': 'Gender_minorities', 'trans': 'Trans', 'man': 'Man', 'wom': 'Women',
                  'overw': 'Overweight', 'skc': 'Skin_color', 'nw': 'Non_white', 'w': 'White', 'bla': 'Black',
                  'ethnic': 'Race_Ethnicity', 'arab': 'Arabs', 'asi': 'Asia', 'east': 'East_A', 's_e': 'South_east_A',
                  'south': 'South_A', 'bla_p': 'Black_people', 'europe': 'Europe', 'east': 'East_E', 'hispanic': 'Hispanic',
                  'indig': 'Indigenous', 'abo': 'Aboriginal_people', 'minority': 'Minority_groups',
                  'mixed': 'Mixed_race', 'african': 'People_from_Africa', 'trav': 'Travelers', 'roma': 'Roma',
                  'religion': 'Religion_or_belief', 'hin': 'Hindus', 'jew': 'Jews', 'mus': 'Muslims',
                  'other_r': 'Other_R', 'sexu': 'Sexuality', 'bis': 'Bisexual', 'gay': 'Gay', 'les': 'Lesbian',
                  'types_hate': 'types_of_hate', 'ani': 'Animosity', 'deh': 'Dehumanization', 'der': 'Derogation',
                  'support': 'Support_for_hateful_entities', 'threat': 'Threatening_language'}

    def get_match_id(self):
        return self.match_id

    def get_match_name(self):
        return self.match_name

    def get_parent_ids(self, id):
        matched = []
        if id >= 60:
            matched.append(60)
        else:
            matched.append(2)
            for element in self.secound_level_groups:
                if id >= element[1][0] - 1 and id <= element[1][1]:
                    matched.append(element[1][0] - 1)
            for element in self.third_level_groups:
                if id >= element[1][0] - 1 and id <= element[1][1]:
                    matched.append(element[1][0] - 1)
            for element in self.frouth_level_groups:
                if id >= element[1][0] - 1 and id <= element[1][1]:
                    matched.append(element[1][0] - 1)

        return matched