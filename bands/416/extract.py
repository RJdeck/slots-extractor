# Description: 从har文件中提取slot数据，写入slot_log.json文件

import json
import os


def extract_to_log(save_file_name='slot_log.json', endswith='.har'):
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
                # print(entry["_resourceType"])
                raw_websocket = entry["_webSocketMessages"]
                for raw_data in raw_websocket:
                    raw_data = json.dumps(raw_data["data"])

                    # 检查是否包含分隔符 ':::',然后解析json数据(两次消除转义符号)
                    if ':::' in raw_data:
                        data_str = raw_data.split(':::', 1)[1]
                        data_json = json.loads('"'+data_str)
                        data_json = json.loads(data_json)
                        if 'windowId' in data_json.get('data', {}):
                            try:
                                slot_data = data_json["data"]["gameData"]["playStack"]

                                # add betCost
                                for slot in slot_data:
                                    slot["betCost"] = data_json["data"]["betCost"]

                                slot_data_list.append(slot_data)
                            except KeyError:
                                print(
                                    f"Error: {KeyError} in {file_name} \n")
                                continue
                        else:
                            continue
                    else:
                        continue
        except KeyError:
            print(f"Error: {file_name} is not a valid har file.")
            continue

    # 在所有数据处理完毕后，将收集到的数据写入文件
    with open(save_file_name, 'w') as slot_log_file:
        json.dump(slot_data_list, slot_log_file, indent=4)
