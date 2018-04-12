from ptsa.data.readers import BaseEventReader
import pandas
import numpy as np
from os import listdir
import os.path

old_events = BaseEventReader(filename='/Users/solbergh/Desktop/events.mat', common_root='', use_reref_eeg = False, eliminate_events_with_no_eeg=False).read()

def add_anns_to_events_recarray(ann_folder_path, events_recarray):
    if (len(events_recarray) == 0):
        print ("Please pass in the recarray from convert_unity_jsonl_to_recarray")
        return
    
    subject = events_recarray[0][0]
    session = events_recarray[0][1]
    
    files_in_folder = listdir(ann_folder_path)
    ann_files = [file for file in files_in_folder if file[-4:] == ".ann"]
    ann_files_to_start_time = {}

    for event in events_recarray:
        if event[4] == "REC_START":
            inferred_ann_name = str(event[2]) + ".ann"
            ann_files_to_start_time[inferred_ann_name] = event[15]
        if event[4] == "CUED_REC_CUE":
            inferred_ann_name = str(event[2]) + "-" + str(event[6]) + ".ann"
            ann_files_to_start_time[inferred_ann_name] = event[15]
        if event[4] == "SR_START":
            inferred_ann_name = "store recall.ann"
            ann_files_to_start_time[inferred_ann_name] = event[15]
        if event[4] == "FFR_START":
            inferred_ann_name = "final recall.ann"
            ann_files_to_start_time[inferred_ann_name] = event[15]

    new_events = []

    for ann_file in ann_files:
        ann_file_path = os.path.join(ann_folder_path, ann_file)
        
        if (ann_file not in ann_files_to_start_time):
            print("WARNING: I couldn't find a corresponding event for .ann file: " + ann_file)
            continue
        start_time = ann_files_to_start_time[ann_file]
        
        ann_lines = []
        with open(ann_file_path) as f:
            trial = -999
            split_index = 0
            if '-' in ann_file:
                split_index = ann_file.index('-')
            else:
                split_index = ann_file.index('.')
            trial_string = ann_file[:split_index]
            try:
                trial = int(trial_string)
            except ValueError:
                pass
            
            ann_lines = f.readlines()
        for line in ann_lines:
            line = line[:-1]
            if len(line) == 0 or line[0] == "#":
                continue
            recall_data = line.split("\t") #time in wav file, word number, word
            type = "REC_WORD"
            mstime = start_time + float(recall_data[0])
            itemno = int(recall_data[1])
            item = recall_data[2]
            word_recarray_entry = (subject, session, trial, -999, type, item, -999, -999, -999, -999, -999, itemno, -999, -999, -999, mstime, -999, -999, -999, -999, -999, -999, -999, -999)
            new_events.append(word_recarray_entry)

    all_events = sorted(new_events + list(events_recarray), key = lambda event: event[15])
    
    new_recarray = np.array(all_events, dtype=[('subject', np.str_, 256), ('session', np.str_, 256), ('trial', int), ('serialPos', int), ('type', np.str_, 256), ('item', np.str_, 256), ('store', np.str_, 256), ('storeX', float), ('storeZ', float), ('presX', float), ('presZ', float), ('itemno', int), ('recalled', int), ('intruded', int), ('finalrecalled', int), ('mstime', int), ('rectime', float), ('intrusion', int), ('eegfile', float), ('eegoffset', int), ('micoffset', int), ('micfile', np.str_, 256), ('correctPointingDirection', float), ('submittedPointingDirection', float)])
    
    return new_recarray



def convert_unity_jsonl_to_recarray(jsonl_file_path):
    new_events = pandas.read_json(path_or_buf=jsonl_file_path, lines=True)

    subject = ""
    session = ""
    if "session_" in jsonl_file_path:
        session_folder_index = jsonl_file_path.index("session_")
        session_folder_and_after = jsonl_file_path[session_folder_index:]
        session_string = ""
        if "_annotated" in session_folder_and_after:
            annoted_index = session_folder_and_after.index("_annotated")
            session_string = session_folder_and_after[8:annoted_index]
        else:
            slash_index = session_folder_and_after.index("/")
            session_string = session_folder_and_after[8:slash_index]
        session = int(session_string)
    trial = 0
    serialPos = ""
    type = ""
    item = ""
    store = ""
    storeX = ""
    storeZ = ""
    presX = ""
    presZ = ""
    itemno = -999
    mstime = 0
    cued_recall_prompt_displayed = False
    cued_recall_stars_displayed = False
    cued_recall_cues_reported = 0
    object_recall_prompt_displayed = False
    object_recall_stars_displayed = False

    recall_events_list = []
    events_list = []
    last_four_text_clears = []
    
    # iterrate through json events converting some and keeping track of relevant fields
    for index, row in new_events.iterrows():
        data = new_events['data'][index]
        
        subject = data['participant 1']
        mstime = int(row.time)
        item = ""
        serialPos = -999
        store = ""
        storeX = -999
        storeZ = -999

        if (row.type == "proceed to next day prompt"):
            trial += 1
        if row.type == "Player transform":
            presX = data['positionX']
            presZ = data['positionZ']
        if row.type == "object presentation begins":
            type = "WORD"
            item = data['item name']
            serialPos = data['serial position']
            store = data['store name']
            storeX = data['store position'][0]
            storeZ = data['store position'][1]
            word_recarray_entry = (subject, session, trial, serialPos, type, item, store, storeX, storeZ, presX, presZ, itemno, -999, -999, -999, mstime, -999, -999, -999, -999, -999, -999, -999, -999)
            events_list.append(word_recarray_entry)
        if (row.type == "pointing begins"):
            type = "pointing begins"
            word_recarray_entry = (subject, session, trial, serialPos, type, item, store, storeX, storeZ, presX, presZ, itemno, -999, -999, -999, mstime, -999, -999, -999, -999, -999, -999, -999, -999)
            events_list.append(word_recarray_entry)
        if (row.type == "pointing finished"):
            correct_direction = data['correct direction (degrees)']
            pointed_direction = data['pointed direction (degrees)']
            type = row.type
            word_recarray_entry = (subject, session, trial, serialPos, type, item, store, storeX, storeZ, presX, presZ, itemno, -999, -999, -999, mstime, -999, -999, -999, -999, -999, -999, correct_direction, pointed_direction)
            events_list.append(word_recarray_entry)
        if (row.type == "display day objects recall prompt" or (row.type == "press any key prompt" and "recall all objects" in data['displayed text'])):
            object_recall_prompt_displayed = True
        if (row.type == "display day cued recall prompt" or (row.type == "press any key prompt" and "recall which object you delivered to the store shown on the screen" in data['displayed text'])):
            cued_recall_prompt_displayed = True
        if (row.type == "display recall text") and cued_recall_prompt_displayed and cued_recall_cues_reported == 0:
            cued_recall_stars_displayed = True
        if (row.type == "display recall text") and object_recall_prompt_displayed:
            object_recall_stars_displayed = True
        if (row.type == "text display cleared"):
            last_four_text_clears.append(row)
            if (len(last_four_text_clears) > 4):
                last_four_text_clears.pop(0)
            if (object_recall_stars_displayed):
                object_recall_stars_displayed = False
                object_recall_prompt_displayed = False
                type = "REC_START"
                word_recarray_entry = (subject, session, trial, serialPos, type, item, store, storeX, storeZ, presX, presZ, itemno, -999, -999, -999, mstime, -999, -999, -999, -999, -999, -999, -999, -999)
                events_list.append(word_recarray_entry)
            if (cued_recall_stars_displayed):
                cued_recall_cues_reported += 1
                if (cued_recall_cues_reported == 12):
                    cued_recall_prompt_displayed = False
                    cued_recall_stars_displayed = False
                    cued_recall_cues_reported = 0
                type = "CUED_REC_CUE"
                word_recarray_entry = (subject, session, trial, serialPos, type, item, store, storeX, storeZ, presX, presZ, itemno, -999, -999, -999, mstime, -999, -999, -999, -999, -999, -999, -999, -999)
                events_list.append(word_recarray_entry)

    if (len(last_four_text_clears) == 4):
        sr_row = last_four_text_clears[1]
        ffr_row = last_four_text_clears[3]
        data = sr_row['data']
        subject = data['participant 1']
        mstime = int(sr_row.time)
        events_list.append((subject, session, -999, -999, "SR_START", "", "", -999, -999, -999, -999, -999, -999, -999, -999, mstime, -999, -999, -999, -999, -999, -999, -999, -999))
        data = ffr_row['data']
        subject = data['participant 1']
        mstime = int(ffr_row.time)
        events_list.append((subject, session, -999, -999, "FFR_START", "", "", -999, -999, -999, -999, -999, -999, -999, -999, mstime, -999, -999, -999, -999, -999, -999, -999, -999))
    

    for index, row in new_events.iterrows():
        better_rec_start_found = False
        unwanted_events = []
        if (row.type == "cued recall recording start"):
            better_rec_start_found = True
            for event in events_list:
                if event[4] == "CUED_REC_CUE" or event[4] == "SR_START" or event[4] == "FFR_START" or event[4] == "SR_STOP" or event[4] == "FFR_STOP" or event[4] == "REC_START":
                    unwanted_events.append(event)
            for event in unwanted_events:
                events_list.remove(event)

        if (better_rec_start_found):
            continue

    for index, row in new_events.iterrows():
        data = new_events['data'][index]
        subject = data['participant 1']
        mstime = int(row.time)
        if (row.type == "cued recall recording start"):
            storeX = data['store position'][0]
            storeZ = data['store position'][1]
            word_recarray_entry = (subject, data['session number'], data['trial number'], -999, 'CUED_REC_CUE', data['item'], data['store'], storeX, storeZ, -999, -999, -999, -999, -999, -999, mstime, -999, -999, -999, -999, -999, "", -999, -999)
            events_list.append(word_recarray_entry)
        if (row.type == "familiarization store displayed"):
            word_recarray_entry = (subject, data['session number'], -999, -999, 'STORE_FAM', '-999', data['store name'], -999, -999, -999, -999, -999, -999, -999, -999, mstime, -999, -999, -999, -999, -999, "", -999, -999)
            events_list.append(word_recarray_entry)
        if (row.type == "final store recall recording start"):
            type = "SR_START"
            word_recarray_entry = (subject, data['session number'], -999, -999, type, "", "", -999, -999, -999, -999, -999, -999, -999, -999, mstime, -999, -999, -999, -999, -999, -999, -999, -999)
            events_list.append(word_recarray_entry)
        if (row.type == "final object recall recording start"):
            type = "FFR_START"
            word_recarray_entry = (subject, data['session number'], -999, -999, type, "", "", -999, -999, -999, -999, -999, -999, -999, -999, mstime, -999, -999, -999, -999, -999, -999, -999, -999)
            events_list.append(word_recarray_entry)
        if (row.type == "final store recall recording stop"):
            type = "SR_STOP"
            word_recarray_entry = (subject, data['session number'], -999, -999, type, "", "", -999, -999, -999, -999, -999, -999, -999, -999, mstime, -999, -999, -999, -999, -999, -999, -999, -999)
            events_list.append(word_recarray_entry)
        if (row.type == "final object recall recording stop"):
            type = "FFR_STOP"
            word_recarray_entry = (subject, data['session number'], -999, -999, type, "", "", -999, -999, -999, -999, -999, -999, -999, -999, mstime, -999, -999, -999, -999, -999, -999, -999, -999)
            events_list.append(word_recarray_entry)
        if (row.type == "object recall recording start"):
            type = "REC_START"
            word_recarray_entry = (subject, data['session number'], data['trial number'], -999, type, "", "", -999, -999, -999, -999, -999, -999, -999, -999, mstime, -999, -999, -999, -999, -999, -999, -999, -999)
            events_list.append(word_recarray_entry)
        if (row.type == "object recall recording stop"):
            type = "REC_STOP"
            word_recarray_entry = (subject, data['session number'], data['trial number'], -999, type, "", "", -999, -999, -999, -999, -999, -999, -999, -999, mstime, -999, -999, -999, -999, -999, -999, -999, -999)
            events_list.append(word_recarray_entry)

    events_list = sorted(events_list, key = lambda event: event[15])

    new_recarray = np.array(events_list, dtype=[('subject', np.str_, 256), ('session', np.str_, 256), ('trial', int), ('serialPos', int), ('type', np.str_, 256), ('item', np.str_, 256), ('store', np.str_, 256), ('storeX', float), ('storeZ', float), ('presX', float), ('presZ', float), ('itemno', int), ('recalled', int), ('intruded', int), ('finalrecalled', int), ('mstime', int), ('rectime', float), ('intrusion', int), ('eegfile', float), ('eegoffset', int), ('micoffset', int), ('micfile', np.str_, 256), ('correctPointingDirection', float), ('submittedPointingDirection', float)])

    return new_recarray
