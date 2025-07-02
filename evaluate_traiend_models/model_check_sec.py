from utility.matching import Matcher
from utility.data_loader import DataLoader
from sklearn.metrics import classification_report
import numpy as np

def run():
    templates_predicted = DataLoader.load_file_csv("resources/predict_evaluation_test_set_round_2_70_30_05_05.csv")
    templates_predicted['vector_2'] = templates_predicted['vector']
    print(len(templates_predicted))

    for index, row in templates_predicted.iterrows():
        sample = list(
            map(float, list(
                filter(None, row['vector_2'].replace('[', '').replace(',', '').replace(']', '').replace('\n', '').split(' ')))))
        if sample[11] == 1:
            templates_predicted = templates_predicted.drop([index])


    print(len(templates_predicted))

    sets = ['vitgen', 'IMSyPP','IMSyPP_no_hate', 'conan']
    for set in sets:
        evlauate_prediction(templates_predicted, set)


def evlauate_prediction(df, set):
    print(set)
    df = df.loc[df['data_set'] == set]
    print(df)

    matcher = Matcher()
    match_id = matcher.get_match_id()

    y_true = df["vector"].to_numpy()
    y_true_float = []
    for sample in y_true:
        #print(sample)
        sample = list(
            map(float, list(filter(None, sample.replace('[', '').replace(',', '').replace(']', '').replace('\n', '').split(' ')))))
        y_true_float.append(sample)
    y_true = y_true_float
    y_scores = df["Raw_Prediction"].to_numpy()

    y_pred = []
    for sample in y_scores:
        sample = list(
            map(float, list(filter(None, sample.replace('[', '').replace(']', '').replace('\n', ' ').split(' ')))))
        y_pred.append([1 if i >= 0.5 else 0 for i in sample])

    if set == 'IMSyPP' or set == 'IMSyPP_no_hate':
        y_pred_new = []
        for vec in y_pred:
            new_vec = []
            for index in range(2,66):
                vec[index] = 0
            new_vec.append(vec)
            y_pred_new.append(new_vec[0])

        y_pred = y_pred_new

    y_pred = np.array(y_pred)

    label_names = list(match_id.keys())

    print(classification_report(y_true, y_pred, target_names=label_names))

if __name__ == '__main__':
    run()
