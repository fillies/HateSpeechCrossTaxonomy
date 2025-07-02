from utility.data_loader import DataLoader
from utility.matching import Matcher
import pandas as pd
pd.set_option('display.max_colwidth', None)



def run():
    conan = DataLoader.load_file_csv("resourcen/conan.csv")[['HATE_SPEECH','TARGET','Prediction_id','Prediction','Raw_Prediction']]#.dropna()

    print(set(list(conan['TARGET'])))
    matcher = Matcher()

    conan["target_new"] = None
    conan["type_new"] = None
    conan["target_binary_vec"] = None



    for index, row in conan.iterrows():
        target = row['TARGET']
        if target != 'other':
            raw_vec = row['Raw_Prediction']
            new_targets = []
            vec = [0] * 66
            combined_binary_vec = [0] * 66

            if target == 'WOMEN':
                new_targets.append(28)
                parents = matcher.get_parent_ids(28)
                for parent in parents:
                    vec[parent] = 1
                vec[1] = 1
                vec[28] = 1
                combined_binary_vec[1] = 1
                combined_binary_vec[28] = 1

            if target == 'LGBT+':
                new_targets.append(11)
                parents = matcher.get_parent_ids(11)
                for parent in parents:
                    vec[parent] = 1
                vec[1] = 1
                vec[11] = 1

            if target == 'POC':
                new_targets.append(32)
                parents = matcher.get_parent_ids(32)
                for parent in parents:
                    vec[parent] = 1
                vec[1] = 1
                vec[32] = 1
                combined_binary_vec[1] = 1
                combined_binary_vec[32] = 1
            #if target == 'other':
            #    vec = raw_vec

            if target == 'JEWS':
                new_targets.append(53)
                parents = matcher.get_parent_ids(53)
                for parent in parents:
                    vec[parent] = 1
                vec[1] = 1
                vec[53] = 1
                combined_binary_vec[1] = 1
                combined_binary_vec[53] = 1
            if target == 'MIGRANTS':
                new_targets.append(8)
                parents = matcher.get_parent_ids(8)
                for parent in parents:
                    vec[parent] = 1
                vec[1] = 1
                vec[8] = 1
                combined_binary_vec[1] = 1
                combined_binary_vec[8] = 1
            if target == 'MUSLIMS':
                new_targets.append(54)
                parents = matcher.get_parent_ids(54)
                for parent in parents:
                    vec[parent] = 1
                vec[1] = 1
                vec[54] = 1
                combined_binary_vec[1] = 1
                combined_binary_vec[54] = 1
            if target == 'DISABLED':
                new_targets.append(23)
                parents = matcher.get_parent_ids(23)
                for parent in parents:
                    vec[parent] = 1
                vec[1] = 1
                vec[23] = 1
                combined_binary_vec[1] = 1
                combined_binary_vec[23] = 1


            conan['target_new'][index] = new_targets
            #conan['type_new'][index] = new_types
            #conan['target_new_vec'][index] = vec
            conan['target_binary_vec'][index] = vec

        else:
            conan = conan.drop([index])

        # vitgen.ix[index,'new_label'] = new_targets

    #print(conan)
    #conan = conan.dropna()
    #print(conan)
    '''targets = ['POC', 'JEWS', 'MUSLIMS', 'WOMEN', 'MIGRANTS', 'DISABLED', 'LGBT+']

    first_level = []
    secound_level = ['LGBT+','JEWS','MIGRANTS','MUSLIMS','DISABLED']
    third_level = ['WOMEN','POC']
    '''
    '''print('all')

    print_over_all_evaluate_results(conan,targets)

    print('secound')

    print_over_all_evaluate_results(conan, secound_level)

    print('third')

    print_over_all_evaluate_results(conan, third_level)

    print('individual word')

    for word in targets:
        print_over_all_evaluate_results(conan, [word])
'''

    print(conan.reset_index(drop=True))
    #print(conan['target_new_vec'].head(1))
    print('Done')

    conan.to_csv('conan_transformed.csv', index=False)



if __name__ == '__main__':
    run()