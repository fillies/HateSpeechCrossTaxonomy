from utility.data_loader import DataLoader
from utility.matching import Matcher
import pandas as pd
pd.set_option('display.max_colwidth', None)



def run():
    vitgen = DataLoader.load_file_csv("resources/vitgen.csv")[['text','label','type','target']].dropna()

    matcher = Matcher()
    match_id = Matcher.get_match_id(matcher)
    match_name = Matcher.get_match_name(matcher)

    no_target = ['none', 'notgiven','notargetrecorded']


    vitgen = vitgen.loc[~vitgen['target'].isin(no_target)]

    vitgen["target_new"] = None
    vitgen["type_new"] = None
    vitgen["target_new_vec"] = None

    for index, row in vitgen.iterrows():
        target = row['target']
        type = row['type']
        new_targets = []
        new_types = []
        sub_targets = target.replace("'", "").replace(" ", "").split(',')
        sub_types = type.replace("'", "").replace(" ", "").split(',')
        excluded_label = ['race']
        vec = [0] * 66

        if 'non.white.wom' in sub_targets:
            sub_targets.extend(['nw', 'wom'])
            sub_targets.remove('non.white.wom')


        for sub in sub_targets:
            if sub == 'non.white':
                sub = 'nw'
            if sub == 'old.people':
                sub = 'age'
            if sub == 'other.religion':
                sub = 'other_r'
            if sub == 'other.national':
                sub = 'other_n'
            if sub == 'non.white.wom':
                pass
            if sub == 'nazis':
                sub = 'support'
            if sub == 'hitler':
                sub = 'support'

            if '.' in sub:
                subs = sub.split('.')
                for sub in subs:
                    if sub == 'eastern':
                        sub = 'east'
                    if sub in match_name and sub not in excluded_label:
                        new_targets.append(match_id[match_name[sub]])

                        parents = matcher.get_parent_ids(match_id[match_name[sub]])
                        for parent in parents:
                            vec[parent] = 1

                        vec[1] = 1
                        vec[match_id[match_name[sub]]] = 1
                    else:
                        if sub not in excluded_label:
                            print(subs)

            else:
                if sub in match_name:

                    if match_id[match_name[sub]] != 64:
                        new_targets.append(match_id[match_name[sub]])
                    else:
                        new_types.append(match_id[match_name[sub]])
                    parents = matcher.get_parent_ids(match_id[match_name[sub]])
                    for parent in parents:
                        vec[parent] = 1

                    vec[1] = 1
                    vec[match_id[match_name[sub]]] = 1
                else:
                    print(sub)

            for sub in sub_types:
                if sub == 'derogation':
                    sub = 'der'
                if sub == 'animosity':
                    sub = 'ani'
                if sub == 'dehumanization':
                    sub = 'deh'
                if sub == 'threatening':
                    sub = 'threat'

                if '.' in sub:
                    subs = sub.split('.')
                    for sub in subs:
                        if sub in match_name and sub not in excluded_label:
                            new_types.append(match_id[match_name[sub]])
                            parents = matcher.get_parent_ids(match_id[match_name[sub]])
                            for parent in parents:
                                vec[parent] = 1
                            vec[1] = 1
                            vec[match_id[match_name[sub]]] = 1
                        else:
                            if sub not in excluded_label:
                                print(subs)

                else:
                    if sub in match_name:
                        new_types.append(match_id[match_name[sub]])

                        parents = matcher.get_parent_ids(match_id[match_name[sub]])
                        for parent in parents:
                            vec[parent] = 1

                        vec[1] = 1
                        vec[match_id[match_name[sub]]] = 1
                    else:
                        print(sub)




        print(new_targets)
        print(new_types)

        vitgen['target_new'][index] = new_targets
        vitgen['type_new'][index] = new_types
        vitgen['target_new_vec'][index] = vec
        #vitgen.ix[index,'new_label'] = new_targets


    print(vitgen.reset_index(drop=True))
    print(vitgen['target_new_vec'].head(1))
    print('Done')

    vitgen.to_csv('resources/vitgen_transformed.csv',index=False)

if __name__ == '__main__':
    run()