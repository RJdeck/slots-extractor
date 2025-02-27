# Description: 从har文件中提取slot数据，写入slot_log.json文件

from cgitb import text
from curses import raw
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

        har_data = har_content["log"]
        entries = har_data["entries"]
        for entry in entries:
            if entry["_resourceType"] != "xhr":
                continue
            raw_request = entry["request"]
            if raw_request["url"] != "https://stag-casino-client.api.relaxg.net/game/play/":
                continue
            try:
                raw_response = entry["response"]
                response_content = raw_response["content"]
                if response_content["mimeType"] != "application/json" or not response_content.get("text"):
                    continue
                response_text = response_content["text"]
                response_json = json.loads(response_text)

                slot_data_list.append(response_json)
            except KeyError:
                print(f"Error: {file_name} contains invalid data part.")
        continue

    # 在所有数据处理完毕后，将收集到的数据写入文件
    with open(save_file_name, 'w') as slot_log_file:
        json.dump(slot_data_list, slot_log_file, indent=4)

    print("Extracting slot data finished.")
