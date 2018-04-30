import pyqtgraph as pg
import os
import json


def plot_words_from_dir(directory):
    window = pg.GraphicsWindow()
    window.resize(2000, 500)
    
    for i in range(3):
        words_file = directory + "/" + str(i) + ".words"
        plot_unityepl(window, words_file)
 
    window.nextRow()

    for i in range(3):
        ann_file = directory + "/" + str(i) + ".ann"
        plot_ann(window, ann_file)

    window.nextRow()

    plot_json(window, directory, 3)
        

    pg.QtGui.QApplication.instance().exec_()


def plot_json(window, directory, trials_to_plot):

    json_file_path = os.path.join(directory, "event_log.json")
    
    with open(json_file_path) as data_file:    
        json_data = json.load(data_file)

    trials = 0
    xsets = []
    trial_start = 0
    for event in json_data['events']:
        if event['event_label'] == "RETRIEVAL" and event["event_value"] == True:            
            trials += 1
            trial_start = event['orig_timestamp']
            xsets = []

        if event['event_label'] == "VOCALIZATION":
            within_recall_timestamp = event['orig_timestamp'] - trial_start
            xsets.append(int(within_recall_timestamp))
            
        if event['event_label'] == "RETRIEVAL" and event["event_value"] == False:
            plot_by_xsets(xsets, "pyepl", window)
            if (trials == trials_to_plot):
                break


def plot_ann(window, ann_file):
    ann_file_lines = []
    with open(ann_file) as f:
        ann_file_lines = f.readlines()

    ann_file_lines = [line.strip() for line in ann_file_lines if line[0] != '#' and len(line) > 1]
        
    word_xsets = []
    for line in ann_file_lines:
        xsets = line.split('\t')
        word_xsets.append(float(xsets[0]))
        word_xsets.append(float(xsets[0])+1)
    word_xsets = [int(xset) for xset in word_xsets]

    plot_by_xsets(word_xsets, ann_file, window)   


def plot_unityepl(window, words_file):
    words_file_lines = []
    with open(words_file) as f:
        words_file_lines = f.readlines()

    words_file_lines = [line.strip() for line in words_file_lines]
        
    word_xsets = []
    for line in words_file_lines:
        xsets = line.split(' ')
        word_xsets.append(float(xsets[0])*1000)
        word_xsets.append(float(xsets[1])*1000)
    word_xsets = [int(xset) for xset in word_xsets]

    plot_by_xsets(word_xsets, words_file, window)


def plot_by_xsets(word_xsets, title, window):
    print(word_xsets)
    someone_speaking = False
    speaking_by_ms = []

    for i in range(1000*30):
        if (len(word_xsets) == 0):
            continue
        if word_xsets[0] == i:
            word_xsets.pop(0)
            someone_speaking = not someone_speaking
        if someone_speaking:
            speaking_by_ms.append(1)
        else:
            speaking_by_ms.append(0)
                      
    word_plot = window.addPlot(title=title, y=speaking_by_ms)
    word_plot.setXRange(0, 30*1000)

 

root_dir = "/users/zduey/Desktop/VAD plot/"
sub_dirs = [f.path for f in os.scandir(root_dir) if f.is_dir()]
for sub_dir in sub_dirs:
    plot_words_from_dir(sub_dir)
