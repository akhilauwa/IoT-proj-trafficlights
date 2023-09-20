import requests

header = {"Content-Type": "application/json"}

while True:
    val = requests.get(
        "https://blynk.cloud/external/api/get?token=6PafxZoNXxmj3ScK7qyjMBngBUaG0oA9&v2",
        headers=header,
    )
    print("pot = " + val.text)
