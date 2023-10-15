import requests

header = {"Content-Type": "application/json"}

val = requests.get(
    "https://blynk.cloud/external/api/get?token=jw1NZLXq38HoD_0YzrBQ2xcAIPY59nip&v2",
    headers=header,
)

print("cars count = " + val.text)
