from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import soundfile as sf
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize


def hf_local(text):
    processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
    model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
    vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

    inputs = processor(text=text, return_tensors="pt")

    embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
    speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

    speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)

    sf.write("speech.wav", speech.numpy(), samplerate=16000)


def main():
    text = "here's a guide on how to start the engine. first make sure car in is park. then push the brake pedal and press the engine start button."

    def count_tokens(text):
        tokens = word_tokenize(text)
        return len(tokens)

    def count_words(text):
        text = text.strip()
        words = text.split()
        return len(words)

    # token_count = count_tokens(text)
    # word_count = count_words(text)
    total_length = len(text)
    print("token count:",count_tokens(text))
    print("word count:",count_words(text))
    print("total length:", len(text))

    if total_length > 600   :
        print(f"Text is too long. Total length is {total_length} characters. Please reduce to 550 characters or less.")
    else:
        hf_local(text)
        print("Text to speech conversion complete. Please check the speech.wav file in your current directory.")

if __name__ == "__main__":
    main()