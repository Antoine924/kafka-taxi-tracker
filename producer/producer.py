from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

print("🚕 Producer Kafka démarré…")

# Monuments de Paris
MONUMENTS = [
    {"name": "Tour Eiffel", "lat": 48.8584, "lon": 2.2945},
    {"name": "Arc de Triomphe", "lat": 48.8738, "lon": 2.2950},
    {"name": "Notre-Dame", "lat": 48.852968, "lon": 2.349902},
    {"name": "Sacré-Cœur", "lat": 48.8867, "lon": 2.3431},
    {"name": "Louvre", "lat": 48.8606, "lon": 2.3376},
]

# Position initiale aléatoire dans Paris
current_lat = random.uniform(48.82, 48.90)
current_lon = random.uniform(2.27, 2.40)

# paramètres de trajet
TOTAL_STEPS = 30      # ~30 secondes pour aller d’un point à un autre
step_index = 0        # étape courante du trajet

# départ / arrivée courants
start_lat = current_lat
start_lon = current_lon
destination = random.choice(MONUMENTS)
dest_lat = destination["lat"]
dest_lon = destination["lon"]

print(f"🎯 Nouvelle destination : {destination['name']}")

while True:
    # interpolation linéaire entre start et dest
    t = step_index / TOTAL_STEPS  # t va de 0 à 1
    current_lat = start_lat + t * (dest_lat - start_lat)
    current_lon = start_lon + t * (dest_lon - start_lon)

    print(f"→ Taxi = ({current_lat:.6f}, {current_lon:.6f}) vers {destination['name']}")

    # envoi dans Kafka
    producer.send("taxi_positions", {
        "lat": current_lat,
        "lon": current_lon,
        "destination": destination["name"]
    })

    step_index += 1

    # si on a atteint la destination (ou dépassé le nombre d’étapes)
    if step_index > TOTAL_STEPS:
        # on fixe le nouveau point de départ à l’ancienne destination
        start_lat = dest_lat
        start_lon = dest_lon

        # on choisit un nouveau monument
        destination = random.choice(MONUMENTS)
        dest_lat = destination["lat"]
        dest_lon = destination["lon"]
        step_index = 0

        print(f"🎯 Nouvelle destination : {destination['name']}")

    time.sleep(1)
