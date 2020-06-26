import tensorflow as tf
from tensorflow import keras
from typing import List
import os, re

def cleanse_strings(str: str) -> str:
    at_a_user = re.sub(r"(\w*[@]\w*)", "<USER>", str)
    twitter_link = re.sub(r"(\w*https://.*\s)", "<LINK>", at_a_user)
    return twitter_link

def make_tweet_lists() -> List[str]:
    texts = []

    cur_folder = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(cur_folder, "data/")
    csv_files = [file for file in os.listdir(data_dir) if
                  file.endswith(".csv")]

    for file_name in csv_files:
        if file_name.split(sep="_") in csv_files:
            csv_files.remove(file_name)
            print("removed", file_name)

    for file_name in csv_files:
        with open(os.path.join(data_dir, file_name)) as csv:
            for line in csv:
                texts.append(line)

    texts = list(map(cleanse_strings, texts))

    print(texts)
    return texts


def get_tokenize_tweet_text(texts: List[str]):
    word_index = keras.preprocessing.text.Tokenizer(
        num_words=None,
        filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
        lower=True,
        split=" ",
        char_level=False,
        oov_token="<UNK>",
        document_count=0
    )

    word_index.fit_on_texts(texts)

    # return word_index.texts_to_sequences(texts)
    return word_index

def sequence_pad_tweets(texts, tokenizer):
    sequences = tokenizer.texts_to_sequences(texts)

    padded_sequences = keras.preprocessing.sequence.pad_sequences(sequences,
                                                            padding="post",
                                                            maxlen=80)
    return padded_sequences


if __name__ == "__main__":
    texts = make_tweet_lists()
    tokenizer = get_tokenize_tweet_text(texts)
    print(sequence_pad_tweets(texts, tokenizer)[0])
