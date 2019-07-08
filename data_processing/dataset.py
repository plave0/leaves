import sys
import pandas
import cv2
import os
from pathlib import Path
from tqdm import tqdm
import image_processing.calc as c


def create_dataset():
    '''Loads all images from image dataset, calculates the features,
    and places them in a .csv file. '''

    #Create dict and define all the columns
    data = {}
    data['hw_ratio'] = []
    data['simetry'] = []
    data['circularity'] = []
    data['rectangularity'] = []
    data['ca_ratio'] = []
    data['cc_ratio'] = []
    data['ch_ratio'] = []
    data['cw_ratio'] = []
    data['center_distance_ratio'] = []
    data['label'] = []
    #data['image'] = []

    #Reading target directory
    folder = str(Path(sys.argv[1]).absolute()) #Reads target from cmd arg
    files = os.listdir(folder)

    #Calculating the features
    for file in tqdm(files):

        #Load image
        image_path = os.path.join(folder,file)
        img = cv2.imread(image_path)

        i = file[0:4] #Get file name

        #Read all the features and place them in the dict
        data['hw_ratio'].append(c.calc_hw_ratio(img))
        data['simetry'].append(c.calc_simetry(img))
        data['circularity'].append(c.calc_circularity(img))
        data['rectangularity'].append(c.calc_rectangularity(img))
        data['ca_ratio'].append(c.calc_ca_ratio(img))
        data['cc_ratio'].append(c.calc_cc_ratio(img))
        data['ch_ratio'].append(c.calc_ch_ratio(img))
        data['cw_ratio'].append(c.calc_cw_ratio(img))
        data['center_distance_ratio'].append(c.calc_center_distance_ratio(img))
        data['label'].append(get_label(int(i)))
        #data['image'].append(i)
    

    #Create a pandas Dataframe from the dict and write it into a .csv file
    df = pandas.DataFrame(data)
    new_file = Path('dataset.csv').absolute()
    exported_csv = df.to_csv(new_file,index=False)
    

def get_label(i):
    '''Get leaf label based on the image number.'''
    
    if i in range(1001,1060):
        return "pubescent bamboo"
    elif i in range(1060,1123):
        return "Chinese horse chestnut"
    elif i in range(1552,1617):
        return "Anhui Barberry"
    elif i in range(1123,1195):
        return "Chinese redbud"
    elif i in range(1195,1268):
        return "true indigo"
    elif i in range(1268,1324):
        return "Japanese maple"
    elif i in range(1324,1386):
        return "Nanmu"
    elif i in range(1386,1438):
        return "castor aralia"
    elif i in range(1497,1552):
        return "Chinese cinnamon"
    elif i in range(1438,1497):
        return "goldenrain tree"
    elif i in range(2001,2051):
        return "Big-fruited Holly"
    elif i in range(2051,2114):
        return "Japanese cheesewood"
    elif i in range(2114,2166):
        return "wintersweet"
    elif i in range(2166,2231):
        return "camphortree"
    elif i in range(2231,2291):
        return "Japan Arrowwood"
    elif i in range(2291,2347):
        return "sweet osmanthus"
    elif i in range(2347,2424):
        return "deodar"
    elif i in range(2424,2486):
        return "ginkgo, maidenhair tree"
    elif i in range(2486,2547):
        return "Crape myrtle, Crepe myrtle"
    elif i in range(2547,2613):
        return "oleander"
    elif i in range(2616,2676):
        return "yew plum pine"
    elif i in range(3001,3056):
        return "Japanese Flowering Cherry"
    elif i in range(3056,3111):
        return "Glossy Privet"
    elif i in range(3111,3176):
        return "Chinese Toon"
    elif i in range(3176,3230):
        return "peach"
    elif i in range(3230,3282):
        return "Ford Woodlotus"
    elif i in range(3282,3335):
        return "trident maple"
    elif i in range(3335,3390):
        return "Beale's barberry"
    elif i in range(3390,3447):
        return "southern magnolia"
    elif i in range(3447,3511):
        return "Canadian poplar"
    elif i in range(3511,3564):
        return "Chinese tulip tree"
    elif i in range(3566,3622):
        return "tangerine"

    

if __name__ == '__main__':
    create_dataset()