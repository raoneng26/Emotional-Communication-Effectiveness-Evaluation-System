#generate scriptfile for english audio

import librosa
import os
import csv
import time
from transformers import WhisperProcessor,WhisperForConditionalGeneration

from pydub import AudioSegment
from pydub.silence import split_on_silence,detect_silence
import soundfile as sf


topic='日本核污水排放'

def script_file_generate(id):
    time_s = time.time()
    isExist = os.path.exists('D:\\电磁辐射网络舆情分析系统\\code\\data_weibo\\'+topic+'_500_600\\script\\{0}_script.csv'.format(id))
    if not isExist:
        with open('D:\\电磁辐射网络舆情分析系统\\code\\data_weibo\\'+topic+'_500_600\\script\\{0}_script.csv'.format(id), 'w+', errors='ignore',
                  encoding='utf-8') as f1:

            writer1=csv.writer(f1,delimiter=';')
            writer1.writerow(['starttime','endtime','text'])
            processor = WhisperProcessor.from_pretrained("E:\whisper-large-v2")
            model = WhisperForConditionalGeneration.from_pretrained("E:\whisper-large-v2")
            os.mkdir('audio_{0}'.format(id))
            sound = AudioSegment.from_mp3('D:\\电磁辐射网络舆情分析系统\\code\\data_weibo\\'+topic+'_500_600\\audio\\{0}.wav'.format(id))
            loundness=sound.dBFS
            print(loundness)

            se_list=detect_silence(sound,min_silence_len=750,silence_thresh=loundness-5)
            start=0
            l=len(se_list)
            for i,se in enumerate(se_list):
                middle=(se[0]+se[1])/2
                sound[start:middle].export('audio_{0}/chunk{1}.wav'.format(id,i),format="wav")
                line=[start/1000,middle/1000]
                translation=''
                start=middle

                path='audio_{0}/chunk{1}.wav'.format(id,i)
                speech_array, sampling_rate = librosa.load(path, sr=16000)
                inputs = processor(speech_array, sampling_rate=16000, return_tensors="pt").input_features
                forced_decoder_ids = processor.get_decoder_prompt_ids(language="en", task="transcribe")
                predicted_ids = model.generate(inputs, forced_decoder_ids=forced_decoder_ids)
                transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
                for k in range(len(transcription)):
                    translation = translation + transcription[k]
                line.append(translation)
                writer1.writerow(line)
                if i==l-1:
                    translation=''
                    line = [start/1000,len(sound)/1000]
                    sound[start:len(sound)].export('audio_{0}/chunk{1}.wav'.format(id,i+1),format="wav")
                    path = 'audio_{0}/chunk{1}.wav'.format(id, i+1)
                    speech_array, sampling_rate = librosa.load(path, sr=16000)
                    inputs = processor(speech_array, sampling_rate=16000, return_tensors="pt").input_features
                    forced_decoder_ids = processor.get_decoder_prompt_ids(language="en", task="translate")  # en与zh切换
                    predicted_ids = model.generate(inputs, forced_decoder_ids=forced_decoder_ids)
                    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
                    for i in range(len(transcription)):
                        translation = translation + transcription[i]
                    line.append(translation)
                    writer1.writerow(line)
                #print(line)

        # delete
        for root, dirs, files in os.walk('audio_{0}'.format(id), topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir('audio_{0}'.format(id))
    print(id,'script file has been generated')


    time_e=time.time()
    time_c=time_e-time_s
    print('cost time:',time_c)


def generate_text(id):
    wavpath = "D:/电磁辐射网络舆情分析系统/code/data_weibo/"+topic+"_500_600/audio/" + id + ".wav"
    textpath = "D:/电磁辐射网络舆情分析系统/code/data_weibo/"+topic+"_500_600/text/" + id + ".txt"
    isExist = os.path.exists(textpath)
    if not isExist:
        speech_array, sampling_rate = librosa.load(wavpath, sr=16000)
        processor = WhisperProcessor.from_pretrained("E:\whisper-base")
        model = WhisperForConditionalGeneration.from_pretrained("E:\whisper-base")
        inputs = processor(speech_array, sampling_rate=16000, return_tensors="pt").input_features
        forced_decoder_ids = processor.get_decoder_prompt_ids(language="zh", task="transcribe")
        predicted_ids = model.generate(inputs, forced_decoder_ids=forced_decoder_ids)
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
        translation = ''
        for k in range(len(transcription)):
            translation = translation + transcription[k]

        with open(textpath, 'w+') as f:
            f.writelines(translation)
        print(f"Finished processing {id}")

if __name__ == '__main__':
    txtpath = 'D:\\电磁辐射网络舆情分析系统\\code\\data_weibo\\test_split.txt'
    with open(txtpath, 'r') as f:
        ids = f.readlines()
    for id in ids:
        id = id.strip('\n')
        script_file_generate(id)



