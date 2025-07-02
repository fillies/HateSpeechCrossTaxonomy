import torch
from transformers import AutoTokenizer, RobertaForSequenceClassification, AutoModelForSequenceClassification
from transformers import BertForSequenceClassification, Trainer
from utility.data_loader import DataLoader

def run():
    templates = DataLoader.load_file_csv("resources/evaluation_test_set.csv")
    templates['HATE_SPEECH'] = 'hateful'

    check_fine_tuned(templates)


# Create torch dataset
class Dataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels=None):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        if self.labels:
            item["labels"] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.encodings["input_ids"])

def check_fine_tuned(templates):
    tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-emotion")

    model_path = "resourcen/trained_models/vitgen_80_20_new_label/file11000/output/checkpoint-11000"
    model = AutoModelForSequenceClassification.from_pretrained(model_path, num_labels=66)
    test_trainer = Trainer(model)
    templates["Raw_Prediction"] = 'nan'


    for index, element in templates.iterrows():
        X_test = [element['text']]
        X_test_tokenized = tokenizer(X_test, padding=True, truncation=True, max_length=512)
        test_dataset = Dataset(X_test_tokenized)
        raw_pred, _, _ = test_trainer.predict(test_dataset)
        templates.at[index, 'Raw_Prediction'] = raw_pred[0]
    print(templates)

    DataLoader.save_df_to_csv(templates, 'resources/predicted_evaluation_test_set_round_1.csv')

if __name__ == '__main__':
    run()
