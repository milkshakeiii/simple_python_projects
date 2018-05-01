import pyqtgraph as pg
import os
import json


def plot_words_from_dir(directory):
    window = pg.GraphicsWindow()
    window.resize(2000, 500)

    for i in range(3):
        plot = window.addPlot(title = "VAD timings")
        plot.setXRange(0, 30*1000)
        plot.setYRange(-20, 20)
        
        words_file = directory + "/" + str(i) + ".words"
        plot_unityepl(plot, words_file)

        ann_file = directory + "/" + str(i) + ".ann"
        plot_ann(plot, ann_file)

        plot_json(plot, directory, i)
            

    pg.QtGui.QApplication.instance().exec_()


def plot_json(plot, directory, trial_to_plot):
    print("pyepl")
    json_file_path = os.path.join(directory, "event_log.json")
    
    with open(json_file_path) as data_file:    
        json_data = json.load(data_file)

    trials = 0
    xsets = []
    trial_start = 0
    for event in json_data['events']:
        if event['event_label'] == "RETRIEVAL" and event["event_value"] == True:            
            if (trials == trial_to_plot):
                trial_start = event['orig_timestamp']
                xsets = []

        if event['event_label'] == "VOCALIZATION" and trials == trial_to_plot:
            within_recall_timestamp = event['orig_timestamp'] - trial_start
            xsets.append(int(within_recall_timestamp))
            
        if event['event_label'] == "RETRIEVAL" and event["event_value"] == False:
            if (trials == trial_to_plot):
                plot_by_xsets(xsets, "pyepl", plot, 3, pg.mkPen(color=(255, 0, 0), width=2))
                break
            trials += 1


def plot_ann(plot, ann_file):
    print("ann")
    ann_file_lines = []
    with open(ann_file) as f:
        ann_file_lines = f.readlines()

    ann_file_lines = [line.strip() for line in ann_file_lines if line[0] != '#' and len(line) > 1]
        
    word_xsets = []
    for line in ann_file_lines:
        xsets = line.split('\t')
        word_xsets.append(float(xsets[0]))
        word_xsets.append(float(xsets[0])+50)
    word_xsets = [int(xset) for xset in word_xsets]

    plot_by_xsets(word_xsets, ann_file, plot, 1, pg.mkPen(color=(0, 255, 0), width=2))   


def plot_unityepl(plot, words_file):
    print("unityepl")
    words_file_lines = []
    with open(words_file) as f:
        words_file_lines = f.readlines()

    words_file_lines = [line.strip() for line in words_file_lines]
        
    word_xsets = []
    for line in words_file_lines:
        xsets = line.split(' ')
        word_xsets.append(float(xsets[0])*1000)
        if len(xsets) > 1:
            word_xsets.append(float(xsets[1])*1000)
    word_xsets = [int(xset) for xset in word_xsets]

    plot_by_xsets(word_xsets, words_file, plot, 2, pg.mkPen(color=(255, 255, 255), width=2))


def plot_by_xsets(word_xsets, title, plot, one, pen):
    print(word_xsets)
    someone_speaking = False
    segment_drawn = False
    speaking_by_ms = []
    ms = []
    for i in range(1000*30):
        if (len(word_xsets) == 0):
            continue
        if word_xsets[0] == i:
            word_xsets.pop(0)
            someone_speaking = not someone_speaking
        if someone_speaking:
            speaking_by_ms.append(one)
            ms.append(i)
            segment_drawn = False
        elif not segment_drawn:
            segment_drawn = True
            plot.plot(y=speaking_by_ms, x=ms, pen=pen)
            speaking_by_ms = []
            ms = []

def plot_by_xsets_lines(word_xsets, title, plot, one, pen):
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
            speaking_by_ms.append(one)
        else:
            speaking_by_ms.append(one-1)

    plot.plot(y=speaking_by_ms, pen=pen) 

 

root_dir = "/users/zduey/Desktop/VAD plot/"
sub_dirs = [f.path for f in os.scandir(root_dir) if f.is_dir()]
for sub_dir in sub_dirs:
    plot_words_from_dir(sub_dir)
