from apikey import api_key
import json
import urllib.request
import xlsxwriter


def read_csv(inputfile):
    video_ids = []
    if str(inputfile).endswith("csv"):
        try:
            with open("links.csv") as f:
                data = f.readlines()           
                [video_ids.append(i[17:].strip()) for i in data]
                print(video_ids)

                return video_ids

        except Exception as e:
            print(e)


def populate_dict(video_ids):
    all_data = {}
    for video_id in video_ids:
        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
        json_url = urllib.request.urlopen(url)
        data = json.loads(json_url.read())
        title = data["items"][0]["snippet"]["title"]
        print(f"Opened {title=}")
        description = data["items"][0]["snippet"]["description"]
        print(f"{description[:50]}...\n.")
        all_data[title] = description

    return all_data


def write_to_xlsx(all_data):
    workbook = xlsxwriter.Workbook('Titles&Descriptions.xlsx')
    worksheet = workbook.add_worksheet("_")
    row, col = 0, 0
    for key, value in all_data.items():
        worksheet.write(row, col, key)
        print(f"writing title: {key[:50]}...")
        worksheet.write(row, col+1, value)
        print(f"writing description: {value[:50]}...")
        row += 1
        col = 0

    workbook.close()

def main():
    video_ids = read_csv("links.csv")
    all_data = populate_dict(video_ids)
    write_to_xlsx(all_data)
    #download = input("would you like to download the videos? y/n")
    # if download == "y":
    #     download_videos()
    input('press enter to quit')

if __name__ == "__main__":
    main()