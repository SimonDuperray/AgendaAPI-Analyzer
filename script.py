import json, requests, matplotlib.pyplot as plt, os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('URL')

def store_agenda_in_file(url):
   agendas = requests.get(url).json()
   with open('./data/agendas.json', 'w') as f:
      json.dump(agendas, f, indent=4)
   print("> stored")

def pie(labels, sizes, title):
   colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'red']
   patches, texts, _ = plt.pie(sizes, colors=colors, startangle=90, autopct='%1.1f%%', textprops=dict(color="w"))
   plt.legend(patches, labels, loc="best")
   plt.axis('equal')
   plt.tight_layout()
   plt.title(title)
   plt.show()

# fetch global object
with open('./data/agendas.json', 'r') as f:
   agenda = json.load(f)

# steps repartition
steps_repartition = agenda['steps_repartition']
steps2 = {
   "downstairs": steps_repartition['0'],
   "first floor": steps_repartition['1'],
   "second floor": steps_repartition['2'],
   "third floor": steps_repartition['3'],
   "fourth floor": steps_repartition['4'],
}
pie(steps2.keys(), steps2.values(), "Floors repartition")

# steps nb_hour_per_lesson
nb_hour_per_lesson = agenda['nb_hour_per_lesson']
pie(nb_hour_per_lesson.keys(), nb_hour_per_lesson.values(), "Hours per lesson")

# steps teachers_repartition
teachers_repartition = agenda['teachers_repartition']
pie(teachers_repartition.keys(), teachers_repartition.values(), "Teachers repartition")

# steps lessons_types_repartition
lessons_types_repartition = agenda['lessons_types_repartition']
pie(lessons_types_repartition.keys(), lessons_types_repartition.values(), "Lessons types repartition")

# steps buildings_repartition
buildings_repartition = agenda['buildings_repartition']
pie(buildings_repartition.keys(), buildings_repartition.values(), "Buildings repartition")