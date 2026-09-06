#we need 2 libraries here to install=>1.librosa==>># to edit the files,load the files specifically for audio files
#  2.resemblyzer ==>># it will make the embeddings of those librosa and it comapres the embeddings of those 2(the current voice and the stored voice embeddings)by applying the ml algos

from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np 
import io
import librosa#for audio editing
import streamlit as st


#loading voice encoder
@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()


def get_voice_embedding(audio_bytes):
    try:
        encoder = load_voice_encoder()

        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        wav = preprocess_wav(audio)
        embedding = encoder.embed_utterance(wav)
        return embedding.tolist()
    except Exception as e:
        st.error('Voice recog error')
        return None
    
# define a methos to identify the speaker
def identify_speaker(new_embedding, candidates_dict, threshold=0.65):
    if new_embedding is None or not candidates_dict:
        return None, 0.0

    
    best_sid = None#best student id
    best_score = -1.0#best score
    #one by one get the stored embeddings for the candidates to check similarity check of  the stored embeddings with the new voice embedding
    for sid, stored_embedding in candidates_dict.items():
        if stored_embedding:
            similarity = np.dot(new_embedding, stored_embedding) #how the both vectores at the same points they lie then they are similar<<==this is taking the dot product=>to know the 2 voice are similay or not
            if similarity> best_score:
                best_score = similarity
                best_sid = sid

    if best_score >= threshold:
        return best_sid, best_score
    
    return None, best_score


#define for the bulk audios(means un the class room one by one tell the sttendence bulkly so for this )
def process_bulk_audio(audio_bytes, candidates_dict, threshold=0.65):

    try:
        encoder = load_voice_encoder()

        #librosa provides 2 things audio and sampling rate
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        #librosa will give the splitted audio bytes called segments
        segments = librosa.effects.split(audio, top_db=30)#top_db=30=>Find the loud parts (speech), and remove the very quiet parts around them.and 30 dB means the sound can be up to 30 decibels quieter than the loudest part of your recording then remove the 30 db quiter means silenece part

       
        identified_results = {}

        #one by one start and end of the segments will taken=>to get the actual voice
        for start, end in segments:

            if (end-start) < sr * 0.5:
                continue
            segment_audio = audio[start:end]# getting the actual voice range
            #then presprocess that range of voice we got
            wav = preprocess_wav(segment_audio)
            #get the embeddings of those segment_audios
            embedding = encoder.embed_utterance(wav)

            # then identify the speaker(student)
            sid, score = identify_speaker(embedding, candidates_dict, threshold)

            if sid:
                if sid not in identified_results or score > identified_results[sid]:
                    identified_results[sid] = score

        return identified_results
    except Exception as e:
        st.error('Bulk process error')
        return {}