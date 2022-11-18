import csv
import function as f
from tkinter import filedialog as fd

# path = "/Users/admin/OneDrive - Université de Bourgogne/Thèse/Bissolfzique/2021/Data brutes/Merge_all.csv"
filename = fd.askopenfilename()
# # path = "/Users/admin/Desktop/9030.csv"
all = []
#
with open(filename, newline='') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=';', quotechar='|')
    header = next(csv_reader)
    header1 = next(csv_reader)

    # Parcours du fichier
    for row in csv_reader:
        all.append(row)

sujets = f.extract_long_court_visuel(all, filename)

# # #tri_sujet_homme = f.find_male(all)
#
# bad_guys = f.mauvais_app(all)
#
# tri_sujet_h_mauvais_app = f.remove_subject(all, bad_guys)
#
# sujets = f.extract_long_court(tri_sujet_h_mauvais_app)

# sujets = f.extract_long_court(all)



