# Description: 从har文件中提取slot数据，写入slot_log.json文件

import json
import os
import time


def extract_to_log(save_file_name='slot_log.json', endswith=".har"):
    files = os.listdir("input")

    slot_data_list = []

    for file_name in files:
        # prevent reading non-har files
        if not file_name.endswith(endswith):
            continue
        file_path = os.path.join("input", file_name)
        f = open(file_path, 'r')
        har_content = json.load(f)

        print(f"Extracting {file_name}...")
        try:
            har_data = har_content["log"]
            entries = har_data["entries"]
            for entry in entries:
                if entry["_resourceType"] != "websocket":
                    continue
                raw_websocket = entry["_webSocketMessages"]
                for raw_data in raw_websocket:
                    raw_data = json.dumps(raw_data["data"])
                    
                    data_json = json.loads(raw_data)
                    data_json = json.loads(data_json)
                    # slot_data_list.append(data_json)
                    if 'event' in data_json.get('body', {}) and data_json['body']['event'] == 'SPIN_RESULT':
                        # print(data_json)
                        try:
                            slot_data = data_json["body"]
                            # process = data_json["data"]["debug"]["history"]["data"]["playStack"]

                            # # add betCost
                            # for slot in slot_data:
                            #     slot["betCost"] = data_json["data"]["betCost"]
                            #     slot["process"] = process

                            slot_data_list.append(slot_data)
                        except KeyError:
                            continue

                    else:
                        continue
                    
        except KeyError:
            print(f"Error: {file_name} is not a valid har file.")
            continue

    start_time = time.time()
    print("Extracting finished, writing to file...")

    # 在所有数据处理完毕后，将收集到的数据写入文件
    with open(save_file_name, 'w') as slot_log_file:
        json.dump(slot_data_list, slot_log_file, indent=4)
    print(f"Writing finished, time elapsed: {
          time.time() - start_time} seconds.")
