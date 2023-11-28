import os
import subprocess
import cv2
import time

n = 0
topic="日本核污水排放"
for j in range(10):  # 外层循环j次
    for i in range(1):  # 内层循环i次
        n = n + 1
        path = 'D:\\电磁辐射网络舆情分析系统\\code\\data_weibo\\'+topic+'\\video\\{0}.mp4'.format(n)
        cap = cv2.VideoCapture(path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # 根据分辨率选择不同的缩放参数
        if width > 475 and width < 485 and height > 555 and height < 565:
            scale = '120:140'
        elif width > 850 and width < 855 and height > 475 and height < 485:
            scale = '216:144'
        elif width > 475 and width < 485 and height > 845 and height < 855:
            scale = '144:216'
        elif width > 1070 and width < 1090 and height > 1910 and height < 1930:
            scale = '72:128'
        else:
            scale = '72:128'
            print(n, '视频长宽为', width, '*', height)

        output_video_path = 'D:\\电磁辐射网络舆情分析系统\\code\\data_weibo\\'+topic+'_500_600\\video\\{0}.avi'.format(n)
        output_audio_path = 'D:\\电磁辐射网络舆情分析系统\\code\\data_weibo\\'+topic+'_500_600\\audio\\{0}.wav'.format(n)

        # 如果输出文件不存在，才进行处理
        if not os.path.exists(output_video_path):
            # 分离视频
            ffmpeg_video_string = 'ffmpeg -i {0} -q:v 6 -vf scale={1} {2}'.format(path, scale, output_video_path)
            p = subprocess.Popen(ffmpeg_video_string, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.communicate()
            print(n, '视频处理完成！')

        if not os.path.exists(output_audio_path):
            # 分离音频
            ffmpeg_audio_string = 'ffmpeg -i {0} -acodec pcm_s16le -vn {1}'.format(path, output_audio_path)
            p = subprocess.Popen(ffmpeg_audio_string, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.communicate()
            print(n, '音频处理完成！')

        time.sleep(1)
