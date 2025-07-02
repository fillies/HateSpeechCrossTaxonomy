from utility.data_loader import DataLoader
import pandas as pd
pd.set_option('display.max_colwidth', None)


def run():
    comments = DataLoader.load_file_csv("resourcen/IMSyPP_EN_YouTube_comments_evaluation_no_context.csv")[['Comment_ID','Text','Type','Annotator']].dropna()

    df_new = pd.DataFrame({'text':[],'vector':[],'label':[]})
    vector = [0] * 66
    vector[1] = 1
    text_done = []
    for index, row in comments.iterrows():
        if str(row['Text']) not in text_done:
            row_2 = comments.loc[(comments['Comment_ID'] == row["Comment_ID"]) & (comments['Annotator'] != row["Annotator"])]

            if len(row_2.values) != 0:
                if row_2['Type'].values[0] == row['Type'] and row['Type'] != "0. appropriate":
                    new_row = {'text': str(row['Text']), 'vector': vector, 'label': 'hate'}
                    text_done.append(str(row['Text']))
                    df_new.loc[len(df_new)] = new_row

    print(df_new)

    df_new.to_csv('IMSyPP_hate.csv', index=False)

if __name__ == '__main__':
    run()