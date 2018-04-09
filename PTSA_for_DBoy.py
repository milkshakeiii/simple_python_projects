from ptsa.data.readers import BaseEventReader
import pandas
import numpy as np

old_events = BaseEventReader(filename='/Users/solbergh/Desktop/R1348J_events_sess0.mat', common_root='', use_reref_eeg = False, eliminate_events_with_no_eeg=False).read()

def convert_unity_jsonl_to_recarray(jsonl_file_path):
    new_events = pandas.read_json(path_or_buf=jsonl_file_path, lines=True)

    subject = ""
    session = ""
    trial = -1
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
    cued_recall_stars_displayed = False
    object_recall_prompt_displayed = False
    object_recall_stars_displayed = False

    recall_events_list = []
    events_list = []
    for index, row in new_events.iterrows():
        data = new_events['data'][index]
        
        subject = data['participant 1']
        mstime = int(row.time)
        item = ""
        session = ""
        serialPos = -999
        store = ""
        storeX = -999
        storeZ = -999

        if (row.type == "repeat video prompt" or row.type == "proceed to next day prompt"):
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
            word_recarray_entry = (subject, session, trial, serialPos, type, item, store, storeX, storeZ, presX, presZ, itemno, -999, -999, -999, mstime, -999, -999, -999, -999, -999, -999)
            events_list.append(word_recarray_entry)
        if (row.type == "pointing begins" or row.type == "pointing finished"):
            type = row.type
            word_recarray_entry = (subject, session, trial, serialPos, type, item, store, storeX, storeZ, presX, presZ, itemno, -999, -999, -999, mstime, -999, -999, -999, -999, -999, -999)
            events_list.append(word_recarray_entry)
        if (row.type == "display day objects recall prompt"):
            object_recall_prompt_displayed = True
        if (row.type == "display recall text") and not object_recall_prompt_displayed:
            cued_recall_stars_displayed = True
        if (row.type == "display recall text") and object_recall_prompt_displayed:
            object_recall_prompt_displayed = False
            object_recall_stars_displayed = True
        if (row.type == "text display cleared"):
            if (object_recall_stars_displayed):
                type = "REC_START"
                word_recarray_entry = (subject, session, trial, serialPos, type, item, store, storeX, storeZ, presX, presZ, itemno, -999, -999, -999, mstime, -999, -999, -999, -999, -999, -999)
                events_list.append(word_recarray_entry)
            if (cued_recall_stars_displayed):
                type = "CUED_REC_CUE"
                word_recarray_entry = (subject, session, trial, serialPos, type, item, store, storeX, storeZ, presX, presZ, itemno, -999, -999, -999, mstime, -999, -999, -999, -999, -999, -999)
                events_list.append(word_recarray_entry)
            cued_recall_stars_displayed = False
            object_recall_stars_displayed = False
        if (row.type == "proceed to next day prompt"):
            #correct for overcounting CUED_REC_CUE events
            events_list = events_list[:len(events_list)-1]


    new_recarray = np.array(events_list, dtype=[('subject', np.str_, 256), ('session', np.str_, 256), ('trial', int), ('serialPos', int), ('type', np.str_, 256), ('item', np.str_, 256), ('store', np.str_, 256), ('storeX', float), ('storeZ', float), ('presX', float), ('presZ', float), ('itemno', int), ('recalled', int), ('intruded', int), ('finalrecalled', int), ('mstime', int), ('rectime', float), ('intrusion', int), ('eegfile', float), ('eegoffset', int), ('micoffset', int), ('micfile', np.str_, 256)])

    return new_recarray
