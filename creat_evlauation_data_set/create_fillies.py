from utility.data_loader import DataLoader
import pandas as pd
pd.set_option('display.max_colwidth', None)


def run():

    comments = DataLoader.load_file_csv_semico("resourcen/DiscordChat_annotiert.csv")[['Message_content','Label']]#.dropna()

    df_new = pd.DataFrame({'text':[],'vector':[],'label':[]})

    vector = [0] * 66
    vector[0] = 1
    for index, row in comments.iterrows():

        if row['Label'] == '0':
            new_row = {'text': str(row['Message_content']), 'vector': vector, 'label': 'no_hate'}
            df_new.loc[len(df_new)] = new_row

    print(df_new)

    df_new.to_csv('fillies_no_hate.csv', index=False)

if __name__ == '__main__':
    run()