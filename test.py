from google.cloud import speech

cmn = 'cmn-Hant-TW'
en = 'en-US'
speech_client = speech.Client()
filename = 'voice.wav'
# Loads the audio into memory
with open(filename, 'rb') as stream:
    audio_sample = speech_client.sample(
            stream=stream,
            encoding='LINEAR16',
            sample_rate_hertz=16000,
            )
    responses = audio_sample.streaming_recognize(language_code=cmn,single_utterance=True)
    results = list(responses)
    try:
        print(results[0].alternatives[0].transcript)
    except:
        print('error')
