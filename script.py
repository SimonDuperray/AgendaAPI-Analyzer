import json, requests, matplotlib.pyplot as plt, os
from dotenv import load_dotenv
from fpdf import FPDF
from os import listdir
from datetime import datetime

load_dotenv()

url = os.getenv('URL')

def store_agenda_in_file(url):
   agendas = requests.get(url).json()
   with open('./data/agendas.json', 'w') as f:
      json.dump(agendas, f, indent=4)
   print("> stored")

# store_agenda_in_file(url)

def pie(labels, sizes, title, filename):
   colors = ['#800000', '#9A6324', '#808000', '#469990', '#000075', '#e6194B', '#f58231', '#ffe119', '#bfef45', '#3cb44b', '#42d4f4', '#4363d8', '#911eb4', '#f032e6', '#a9a9a9', '#fabed4', '#ffd8b1', '#fffac8', '#aaffc3', '#dcbeff']
   patches, texts, _ = plt.pie(sizes, colors=colors, radius=1000, startangle=90, autopct='%1.1f%%', textprops=dict(color="w"))
   plt.legend(patches, labels, loc="best")
   plt.axis('equal')
   plt.tight_layout()
   plt.title(title)
   plt.savefig('./figures/' + filename + '.png', bbox_inches='tight')
   plt.clf()

# fetch global object
with open('./data/agendas.json', 'r') as f:
   agenda = json.load(f)

# create and store figures
def create_figures(agenda):
   # steps repartition
   steps_repartition = agenda['steps_repartition']
   steps2 = {
      "downstairs": steps_repartition['0'],
      "first floor": steps_repartition['1'],
      "second floor": steps_repartition['2'],
      "third floor": steps_repartition['3'],
      "fourth floor": steps_repartition['4'],
   }
   pie(steps2.keys(), steps2.values(), "Floors repartition", 'floors_repartition')

   # steps nb_hour_per_lesson
   nb_hour_per_lesson = agenda['nb_hour_per_lesson']
   pie(nb_hour_per_lesson.keys(), nb_hour_per_lesson.values(), "Hours per lesson", "hours_per_lesson")

   # steps teachers_repartition
   teachers_repartition = agenda['teachers_repartition']
   pie(teachers_repartition.keys(), teachers_repartition.values(), "Teachers repartition", "teachers_repartition")

   # steps lessons_types_repartition
   lessons_types_repartition = agenda['lessons_types_repartition']
   pie(lessons_types_repartition.keys(), lessons_types_repartition.values(), "Lessons types repartition", "lessons_types_repartition")

   # steps buildings_repartition
   buildings_repartition = agenda['buildings_repartition']
   pie(buildings_repartition.keys(), buildings_repartition.values(), "Buildings repartition", "buildings_repartition")

   # nb total classes and exams
   nb_total_classes = agenda['nb_hours']
   nb_total_exams = agenda['nb_exams']
   fig = plt.figure()
   ax = fig.add_axes([0,0,1,1])
   labels = ['Classes', 'Exams']
   hours = [nb_total_classes, nb_total_exams]
   ax.bar(labels,hours, width=0.3, color=['#800000', '#e6194B'])
   plt.title('Total classes and exams')
   plt.savefig('./figures/classes_and_exams.png', bbox_inches='tight', dpi=75)
   plt.clf()

   print("> Figures created")

create_figures(agenda)

# write pdf file
def write_pdf():
   today = str(datetime.date(datetime.now()))
   figures = os.listdir('./figures')
   pdf = FPDF(orientation='P')
   pdf.set_auto_page_break(0)
   pdf.add_page(orientation='P')
   pdf.set_font('Arial', 'B', 20)
   pdf.image('./data/eseo.png')
   pdf.text(20, 70, "Weekly Report - "+today)
   pdf.text(20, 80, "Id: "+str(agenda['student_id']))
   pdf.image('./figures/classes_and_exams.png', x=20, y=100)
   for figure in figures:
      if figure!="classes_and_exams.png":
         pdf.add_page(orientation='L')
         pdf.image('./figures/'+figure)
   pdf.output('./reports/test.pdf', 'F')
   print("> PDF file created")
write_pdf()