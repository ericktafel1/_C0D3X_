import requests
import zipfile
import io
import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib
import sys
import json
import joblib

def download():
    url = "https://academy.hackthebox.com/storage/modules/292/skills_assessment_data.zip"
    response = requests.get(url)
    if response.status_code == 200:
        print("Download successful")
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall("skills_assessment_data")
            print("Extraction successful")
    else:
        print("Failed to download the dataset")

def dataset():
    df = pd.read_json("skills_assessment_data/train.json", orient="records")
    df.info()
    # Drop duplicates
    df = df.drop_duplicates()
    return df

def clean_text(text):
    # Remove HTML tags
    text = re.sub(r"<.*?>", " ", text)
    # Remove non-word characters (punctuation, etc.) but keep spaces
    text = re.sub(r"[^\w\s]", " ", text)
    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text

def preprocessing(df):
    # Basic text cleaning
    df["text"] = df["text"].apply(lambda x: x.lower())
    df["text"] = df["text"].apply(clean_text)
    return df

def train_model(df):
    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(
        df["text"], df["label"], test_size=0.3, random_state=42
    )

    # Create the pipeline
    pipeline = Pipeline([
        ("vectorizer", CountVectorizer(
            lowercase=True,
            stop_words="english",
            token_pattern=r"\b\w+\b",
            ngram_range=(1, 2)
        )),
        ("classifier", MultinomialNB())
    ])

    print("Training model...")
    pipeline.fit(X_train, y_train)
    print("Training complete!")

    # Save the trained model
    model_filename = "assessment.joblib"
    joblib.dump(pipeline, model_filename)
    print(f"Model saved to {model_filename}")

    return pipeline

def evaluate_model(model, new_texts):
    print("\nEvaluating new texts:")
    predictions = model.predict(new_texts)
    probabilities = model.predict_proba(new_texts)
    
    for text, pred, prob in zip(new_texts, predictions, probabilities):
        pred_label = "Good" if pred == 1 else "Bad"
        print(f"Text: {text[:60]}...")
        print(f"  -> Prediction: {pred_label} | Probabilities: {prob}")


def upload_model(pipeline):
    target = sys.argv[1]
    url = f'http://{target}:5000/api/upload'

    model_file_path = 'assessment.joblib'
    with open(model_file_path, "rb") as model_file:
        files = {"model": model_file}
        response = requests.post(url, files=files)

    # Pretty print the response from the server
    print(json.dumps(response.json(), indent=4))

if __name__ == "__main__":

    # Check for usage
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <target_ip>')
        sys.exit(1)

    target = sys.argv[1]

    download()
    df = dataset()
    df = preprocessing(df)

    # Train the model
    model = train_model(df)

    # Example new texts
    new_texts = [
	"This movie is amazing because the fact that the real people portray themselves and their real life experience and do such a good job it's like they're almost living the past over again. Jia Hongsheng plays himself an actor who quit everything except music and drugs struggling with depression and searching for the meaning of life while being angry at everyone especially the people who care for him most. There's moments in the movie that will make you wanna cry because the family especially the father did such a good job. However, this movie is not for everyone. Many people who suffer from depression will understand Hongsheng's problem and why he does the things he does for example keep himself shut in a dark room or go for walks or bike rides by himself. Others might see the movie as boring because it's just so real that its almost like a documentary. Overall this movie is great and Hongsheng deserved an Oscar for this movie so did his Dad."
	"I first saw this movie on IFC. Which is a great network by the way to see underground films. I watched this movie and was thinking it was going to be pure drama and a story line that doesn't hold water. But it really was a worth while watch. The main character is in such rough shape, and you hate to see him deny help, but no matter what you just can't hate him. His devotion to The Beatles and John Lennon is a great metaphor for his life and the helplessness he feels. <br /><br />The atmosphere of the film is also great. At times, you feel like you can see what he sees, feel what he feels in some situations. This movie does not leave you wanting to know more, or disliking a loophole in the plot. There are NO loopholes (in my opinion). I have always been a fan of foreign films, especially now with movies being made so poorly in America. I really enjoy the foreign settings because I feel it can take you on a trip, and sometimes understand a different culture. This movie did all those things to me and more. Please watch this movie and if you're new to foreign films, this is a great start."
	"I was surprised how much I enjoyed this. Sure it is a bit slow moving in parts, but what else would one expect from Rollin? Also there is plenty of nudity, nothing wrong with that, particularly as it includes lots of the gorgeous, Brigitte Lahaie. There are also some spectacularly eroticised female dead, bit more dodgey, perhaps, but most effective. There is also a sci-fi like storyline with a brief explanation at the end, but I wouldn't bother too much with that. No, here we have a most interesting exploration of memory and the effect of memory loss and to just what extent one is still 'alive' without memory. My DVD sleeve mentions David Cronenberg and whilst this is perhaps not quite as good as his best films, there is some similarity here, particularly with the great use of seemingly menacing architecture and the effective and creepy use of inside space. As I have tried to indicate this is by no means a rip roaring thriller, it is a captivating, nightmare like movie that makes the very most of its locations, including a stunning railway setting at the end."
    ]


    # Evaluate the model on new texts
    evaluate_model(model, new_texts)
    
    # Upload model and get flag
    upload_model(model)


# Save the trained model to a file for future use
model_filename = 'capstone_model.joblib'
joblib.dump(model, model_filename)

print(f"Model saved to {model_filename}")
