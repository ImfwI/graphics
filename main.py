import cv2
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, TextClip
from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick\magick.exe"})


def process_video(video_path, background_path, logo_path, event_title, output_path):
    """Функция для наложения видео на фон с логотипом и названием ."""
    
    video_clip = VideoFileClip(video_path)
    background_img = ImageClip(background_path).set_duration(video_clip.duration)
    background_img = background_img.resize(newsize=(1920, 1080))
    
    video_clip = video_clip.resize(height=720)
    
    logo = ImageClip(logo_path).set_duration(video_clip.duration).resize(height=int(background_img.h * 0.15))
    
    text_clip = (TextClip(event_title, fontsize=50, color='white', font='Arial-Bold')
                 .set_duration(video_clip.duration)
                 .on_color(size=(TextClip(event_title, fontsize=50).w + 10, 
                                 TextClip(event_title, fontsize=50).h + 10), 
                           color=(0, 0, 0), col_opacity=0.6))
    
    video_position = ('center', 'center')  
    logo_position = ('right', 'bottom')    
    text_position = ('center', 'top')      
    
    final_clip = CompositeVideoClip([
        background_img,
        video_clip.set_position(video_position),
        logo.set_position(logo_position),
        text_clip.set_position(text_position)
    ])
    
    final_clip.write_videofile(output_path, codec="libx264", preset="ultrafast", threads=4, fps=24) 


def load_files():
    """Функция для загрузки файлов через интерфейс и запуска обработки видео."""
    video_path = filedialog.askopenfilename(title="Выберите видео файл", filetypes=[("Видео файлы", "*.mp4 *.avi")])
    background_path = filedialog.askopenfilename(title="Выберите фоновое изображение", filetypes=[("Изображения", "*.png")])
    logo_path = filedialog.askopenfilename(title="Выберите логотип", filetypes=[("Изображения", "*.png")])
    
    event_title = event_title_entry.get()
    
    output_path = "output_video.mp4"
    
    process_video(video_path, background_path, logo_path, event_title, output_path)
    print("Видео успешно создано!")


def create_gui():
    """Функция для создания графического интерфейса."""
    root = Tk()
    root.title("Видеоредактор для трансляций")
    
    Label(root, text="Введите название мероприятия:").pack(pady=10)
    global event_title_entry
    event_title_entry = Entry(root, width=50)
    event_title_entry.pack(pady=10)
    
    Button(root, text="Загрузить видео, фон, логотип и создать", command=load_files).pack(pady=20)
    
    root.mainloop()


if __name__ == '__main__':
    create_gui()
