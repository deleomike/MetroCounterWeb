import requests
import numpy as np
import time
import matplotlib.pyplot as plt

if __name__ == "__main__":

    num = 100000

    data = [np.random.randint(100) for i in range(num)]

    print(data)

    payload = {
        "location": "tysons_corner",
        "num_data_points": num,
        "data": data
    }

    start = time.time()
    requests.post("http://localhost:8000/crowd_data", json=payload)
    print(time.time() - start)

    current = requests.get("http://localhost:8000/crowd_data/tysons_corner/current").json()["value"]
    hour = requests.get("http://localhost:8000/crowd_data/tysons_corner/hour").json()["value"]
    day = requests.get("http://localhost:8000/crowd_data/tysons_corner/day").json()["value"]
    week = requests.get("http://localhost:8000/crowd_data/tysons_corner/week").json()["value"]
    month = requests.get("http://localhost:8000/crowd_data/tysons_corner/month").json()["value"]

    def plot(index, data, title):
        plt.figure(index)
        plt.plot(data)
        plt.title(title)

    plot(0, hour, "Hour")
    plot(1, day, "Day")
    plot(2, week, "Week")
    plot(3, month, "Month")
    plot(4, data, "Raw")

    plt.show()