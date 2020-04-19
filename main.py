from variables import *
import datetime
import os
from game import play_game
import imageio
# import cv2

if __name__ == '__main__':

    folder = str(datetime.datetime.now())
    folder = folder.replace(" ", "-").replace(":", "-")
    print(folder)

    if not os.path.exists(str("data/"+folder)):
        os.makedirs(str("data/"+folder))
        PATH = "data/"+folder
        play_game(PATH)

    files = [f for f in os.listdir(PATH)  if os.path.isfile(os.path.join(PATH, f))]
    with imageio.get_writer('render/'+folder+".gif", mode='I', duration = 0.001) as writer:
        for file in files:
            image = imageio.imread(PATH + '/' + file)
            writer.append_data(image)

        writer.append_data(image)
        writer.append_data(image)
        writer.append_data(image)
        writer.append_data(image)
        writer.append_data(image)

    # video_name = folder+'.avi'
    # images = [img for img in os.listdir(PATH) if img.endswith(".png")]
    # frame = cv2.imread(os.path.join(PATH, images[0]))
    # height, width, layers = frame.shape
    #
    # video = cv2.VideoWriter(video_name, 0, 1, (width, height))
    #
    # for image in images:
    #     video.write(cv2.imread(os.path.join('render/', image)))
    #
    # cv2.destroyAllWindows()
    # video.release()
