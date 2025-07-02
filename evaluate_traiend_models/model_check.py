from utility.matching import Matcher
from utility.data_loader import DataLoader
from sklearn.metrics import classification_report
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import multilabel_confusion_matrix, ConfusionMatrixDisplay


def run():
    templates_predicted = DataLoader.load_file_csv("resources/predicted_evaluation_test_set_round_1.csv")
    sets = ['vitgen', 'IMSyPP','IMSyPP_no_hate', 'conan']
    for set in sets:
        evlauate_prediction(templates_predicted, set)


def evlauate_prediction(df, set):
    print(set)
    df = df.loc[df['data_set'] == set]
    print(df.columns)


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
    print(y_pred)

    counter = 0
    true_lgbtq_vev = []
    true_non_white_vev = []
    target_lgbtq_vev = []
    target_non_white_vev = []
    distibrution_vec = [0]*66
    distibrution_vec_non_white = [0] * 66
    true_distibrution_vec = [0]*66
    true_distibrution_vec_non_white = [0]*66

    for element in y_true:
        #print(element)
        if element[10]==1 and element[11]==1:
            if y_pred[counter][10] != 1 and y_pred[counter][11] != 1:
                true_lgbtq_vev.append(element)
                target_lgbtq_vev.append(y_pred[counter])

        if element[32]==1:
            if y_pred[counter][32] != 1:
                true_non_white_vev.append(element)
                target_non_white_vev.append(y_pred[counter])
        counter += 1


    for index, element in enumerate(distibrution_vec):
        distibrution_vec[index] = sum(x[index] for x in target_lgbtq_vev)
        true_distibrution_vec[index] = sum(x[index] for x in true_lgbtq_vev)

        distibrution_vec_non_white[index] = sum(x[index] for x in target_non_white_vev)
        true_distibrution_vec_non_white[index] = sum(x[index] for x in true_non_white_vev)

    print(distibrution_vec)
    print(true_distibrution_vec)
    print(distibrution_vec_non_white)
    print(distibrution_vec_non_white[33])
    print(true_distibrution_vec_non_white)
    print(true_distibrution_vec_non_white[33])
    matcher = Matcher()
    print('LGBTQ###########################################################')
    for index, element in enumerate(distibrution_vec):
        res = distibrution_vec[index] - true_distibrution_vec[index]
        if res > 0:

            print(list(matcher.get_match_id())[index])
            print(res/465)
            distibrution_vec[index] = res/465

    print('non_white########################################################')
    for index, element in enumerate(distibrution_vec_non_white):
        res = distibrution_vec_non_white[index] - true_distibrution_vec_non_white[index]
        if res > 0:
            print(list(matcher.get_match_id())[index])
            print(res / 296)
            distibrution_vec_non_white[index] = res / 296

    label_names = list(match_id.keys())

    print(classification_report(y_true, y_pred, target_names=label_names))

    if set == 'conan':
        confusion_matrices = multilabel_confusion_matrix(y_true, y_pred)
        index = 0
        for confusion_matrix in confusion_matrices:
            disp = ConfusionMatrixDisplay(confusion_matrix, display_labels=[0,1])
            disp.plot(include_values=True, cmap="viridis", ax=None, xticks_rotation="vertical")
            plt.text(.96, .94, str(label_names[index]), bbox={'facecolor': 'w', 'pad': 5},
                     ha="right", va="top", transform=plt.gca().transAxes)
            index +=1
            plt.show()


if __name__ == '__main__':
    run()
