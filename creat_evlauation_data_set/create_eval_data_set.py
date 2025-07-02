from utility.data_loader import DataLoader
import pandas as pd
pd.set_option('display.max_colwidth', None)

def run():
    vitgen = DataLoader.load_file_csv("resources/vitgen_transformed.csv")[['text','label','type','target','target_new','type_new','target_new_vec']].dropna().rename(columns={"target_new_vec": "vector"})
    IMSyPP = DataLoader.load_file_csv("resources/IMSyPP_hate.csv")[['text','vector','label']].dropna()
    IMSyPP_no_hate = DataLoader.load_file_csv("resources/IMSyPP_no_hate.csv")[['text','vector','label']].dropna()
    conan = DataLoader.load_file_csv("resources/conan_transformed.csv")[['HATE_SPEECH','TARGET','Prediction_id','Prediction','Raw_Prediction','target_new','type_new','target_binary_vec']].rename(columns={"HATE_SPEECH":"text","target_binary_vec": "vector"})#.dropna()

    vitgen['data_set'] = 'vitgen'
    IMSyPP['data_set'] = 'IMSyPP'
    IMSyPP_no_hate['data_set'] = 'IMSyPP_no_hate'
    conan['data_set'] = 'conan'

    combined = pd.concat([vitgen[['text','vector','data_set']],IMSyPP[['text','vector','data_set']],IMSyPP_no_hate[['text','vector','data_set']],conan[['text','vector','data_set']]])

    print(combined)
    print(len(vitgen))
    print(len(IMSyPP))
    print(len(IMSyPP_no_hate))
    print(len(conan))
    print(len(combined))

    combined.to_csv('evaluation_test_set.csv', index=False)

if __name__ == '__main__':
    run()