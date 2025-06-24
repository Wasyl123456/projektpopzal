from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

universities = []
employees = []
students = []

# KLASY

class University:
    def __init__(self, name, voivodeship, district):
        self.name = name
        self.voivodeship = voivodeship
        self.district = district
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=self.name)

    def get_coordinates(self):
        url = f"https://pl.wikipedia.org/wiki/{self.name}"
        response = requests.get(url).text
        soup = BeautifulSoup(response, "html.parser")
        lon = float(soup.select(".longitude")[1].text.replace(",", "."))
        lat = float(soup.select(".latitude")[1].text.replace(",", "."))
        return [lat, lon]

class Employee:
    def __init__(self, name, surname, city, university):
        self.name = name
        self.surname = surname
        self.city = city
        self.university = university
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=f"{self.name} {self.surname}")

    def get_coordinates(self):
        url = f"https://pl.wikipedia.org/wiki/{self.city}"
        response = requests.get(url).text
        soup = BeautifulSoup(response, "html.parser")
        lon = float(soup.select(".longitude")[1].text.replace(",", "."))
        lat = float(soup.select(".latitude")[1].text.replace(",", "."))
        return [lat, lon]

class Student:
    def __init__(self, name, surname, university, group, city, dormitory):
        self.name = name
        self.surname = surname
        self.university = university
        self.group = group
        self.city = city
        self.dormitory = dormitory
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=f"{self.name} {self.surname}")

    def get_coordinates(self):
        url = f"https://pl.wikipedia.org/wiki/{self.city}"
        response = requests.get(url).text
        soup = BeautifulSoup(response, "html.parser")
        lon = float(soup.select(".longitude")[1].text.replace(",", "."))
        lat = float(soup.select(".latitude")[1].text.replace(",", "."))
        return [lat, lon]

def clear_all_markers():
    for u in universities:
        if u.marker: u.marker.delete()
    for e in employees:
        if e.marker: e.marker.delete()
    for s in students:
        if s.marker: s.marker.delete()

# GUI
root = Tk()
root.configure(bg="black")
root.option_add("*Background", "black")
root.option_add("*Foreground", "white")
root.option_add("*Font", "Arial 10")

root.title("System zarządzania uczelniami")
root.geometry("1280x800")

frame_univ = LabelFrame(root, text="Uczelnie", font=("Arial", 11), bg="black", fg="white")
frame_univ.grid(row=0, column=0, padx=10, pady=10, sticky="n")

frame_emp = LabelFrame(root, text="Pracownicy", font=("Arial", 11), bg="black", fg="white")
frame_emp.grid(row=0, column=1, padx=10, pady=10, sticky="n")

frame_stud = LabelFrame(root, text="Studenci", font=("Arial", 11),bg="black", fg="white")
frame_stud.grid(row=0, column=2, padx=10, pady=10, sticky="n")

map_widget = tkintermapview.TkinterMapView(root, width=1200, height=350)
map_widget.set_position(52.23, 21)
map_widget.set_zoom(6)
map_widget.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# UCZELNIE
entry_univ_name = Entry(frame_univ)
entry_voivodeship = Entry(frame_univ)
entry_district = Entry(frame_univ)
entry_voivodeship_filter = Entry(frame_univ)
listbox_univ = Listbox(frame_univ, height=4)

def add_university():
    name = entry_univ_name.get()
    voiv = entry_voivodeship.get()
    dist = entry_district.get()
    u = University(name, voiv, dist)
    universities.append(u)
    entry_univ_name.delete(0, END)
    entry_voivodeship.delete(0, END)
    entry_district.delete(0, END)
    show_universities()

def show_universities():
    listbox_univ.delete(0, END)
    for idx, u in enumerate(universities):
        listbox_univ.insert(END, f"{u.name} ({u.district})")

def show_universities_by_voivodeship():
    clear_all_markers()
    selected = entry_voivodeship_filter.get()
    listbox_univ.delete(0, END)
    for u in universities:
        if u.voivodeship == selected:
            listbox_univ.insert(END, f"{u.name} ({u.district})")
            u.marker = map_widget.set_marker(u.coordinates[0], u.coordinates[1], text=u.name)

def delete_university():
    idx = listbox_univ.index(ACTIVE)
    universities[idx].marker.delete()
    universities.pop(idx)
    show_universities()

def show_university_details():
    idx = listbox_univ.index(ACTIVE)
    u = universities[idx]
    print(f"Uczelnia: {u.name}, Woj: {u.voivodeship}, Pow: {u.district}")

def edit_university():
    idx = listbox_univ.index(ACTIVE)
    u = universities[idx]
    entry_univ_name.insert(0, u.name)
    entry_voivodeship.insert(0, u.voivodeship)
    entry_district.insert(0, u.district)
    btn_add_univ.configure(text="Zapisz", command=lambda: update_university(idx))

def update_university(idx):
    u = universities[idx]
    u.marker.delete()
    u.name = entry_univ_name.get()
    u.voivodeship = entry_voivodeship.get()
    u.district = entry_district.get()
    u.coordinates = u.get_coordinates()
    u.marker = map_widget.set_marker(u.coordinates[0], u.coordinates[1], text=u.name)
    btn_add_univ.configure(text="Dodaj", command=add_university)
    show_universities()
    entry_univ_name.delete(0, END)
    entry_voivodeship.delete(0, END)
    entry_district.delete(0, END)

Label(frame_univ, text="Nazwa:").grid(row=0, column=0)
entry_univ_name.grid(row=0, column=1)
Label(frame_univ, text="Województwo:").grid(row=1, column=0)
entry_voivodeship.grid(row=1, column=1)
Label(frame_univ, text="Powiat:").grid(row=2, column=0)
entry_district.grid(row=2, column=1)
btn_add_univ = Button(frame_univ, text="Dodaj", command=add_university)
btn_add_univ.grid(row=3, column=0, columnspan=2)
Label(frame_univ, text="Filtruj wg województwa:").grid(row=4, column=0)
entry_voivodeship_filter.grid(row=4, column=1)
Button(frame_univ, text="Pokaż", command=show_universities_by_voivodeship).grid(row=5, column=0, columnspan=2)
listbox_univ.grid(row=6, column=0, columnspan=2)
Button(frame_univ, text="Szczegóły", command=show_university_details).grid(row=7, column=0)
Button(frame_univ, text="Edytuj", command=edit_university).grid(row=7, column=1)
Button(frame_univ, text="Usuń", command=delete_university).grid(row=7, column=2)

# PRACOWNICY
entry_emp_name = Entry(frame_emp)
entry_emp_surname = Entry(frame_emp)
entry_emp_city = Entry(frame_emp)
entry_emp_university = Entry(frame_emp)
listbox_emp = Listbox(frame_emp, height=4)

def add_employee():
    name = entry_emp_name.get()
    surname = entry_emp_surname.get()
    city = entry_emp_city.get()
    university = entry_emp_university.get()
    emp = Employee(name, surname, city, university)
    employees.append(emp)
    clear_entries_emp()
    show_employees()

def show_employees():
    listbox_emp.delete(0, END)
    for e in employees:
        listbox_emp.insert(END, f"{e.name} {e.surname} ({e.city})")

def delete_employee():
    idx = listbox_emp.index(ACTIVE)
    employees[idx].marker.delete()
    employees.pop(idx)
    show_employees()

def show_employee_details():
    idx = listbox_emp.index(ACTIVE)
    e = employees[idx]
    print(f"{e.name} {e.surname}, {e.city}, {e.university}")

def edit_employee():
    idx = listbox_emp.index(ACTIVE)
    e = employees[idx]
    entry_emp_name.insert(0, e.name)
    entry_emp_surname.insert(0, e.surname)
    entry_emp_city.insert(0, e.city)
    entry_emp_university.insert(0, e.university)
    btn_add_emp.configure(text="Zapisz", command=lambda: update_employee(idx))

def update_employee(idx):
    e = employees[idx]
    e.marker.delete()
    e.name = entry_emp_name.get()
    e.surname = entry_emp_surname.get()
    e.city = entry_emp_city.get()
    e.university = entry_emp_university.get()
    e.coordinates = e.get_coordinates()
    e.marker = map_widget.set_marker(e.coordinates[0], e.coordinates[1], text=f"{e.name} {e.surname}")
    btn_add_emp.configure(text="Dodaj", command=add_employee)
    clear_entries_emp()
    show_employees()

def clear_entries_emp():
    entry_emp_name.delete(0, END)
    entry_emp_surname.delete(0, END)
    entry_emp_city.delete(0, END)
    entry_emp_university.delete(0, END)

Label(frame_emp, text="Imię:").grid(row=0, column=0)
entry_emp_name.grid(row=0, column=1)
Label(frame_emp, text="Nazwisko:").grid(row=1, column=0)
entry_emp_surname.grid(row=1, column=1)
Label(frame_emp, text="Miasto:").grid(row=2, column=0)
entry_emp_city.grid(row=2, column=1)
Label(frame_emp, text="Uczelnia:").grid(row=3, column=0)
entry_emp_university.grid(row=3, column=1)
btn_add_emp = Button(frame_emp, text="Dodaj", command=add_employee)
btn_add_emp.grid(row=4, column=0, columnspan=2)
listbox_emp.grid(row=5, column=0, columnspan=2)
Button(frame_emp, text="Szczegóły", command=show_employee_details).grid(row=6, column=0)
Button(frame_emp, text="Edytuj", command=edit_employee).grid(row=6, column=1)
Button(frame_emp, text="Usuń", command=delete_employee).grid(row=6, column=2)

#  STUDENCI
entry_stud_name = Entry(frame_stud)
entry_stud_surname = Entry(frame_stud)
entry_stud_university = Entry(frame_stud)
entry_stud_group = Entry(frame_stud)
entry_stud_city = Entry(frame_stud)
entry_group_filter = Entry(frame_stud)
listbox_stud = Listbox(frame_stud, height=4)

def add_student():
    name = entry_stud_name.get()
    surname = entry_stud_surname.get()
    university = entry_stud_university.get()
    group = entry_stud_group.get()
    city = entry_stud_city.get()
    dormitory = entry_stud_dormitory.get()
    s = Student(name, surname, university, group, city, dormitory)
    students.append(s)
    clear_entries_stud()
    show_students()

def show_students():
    listbox_stud.delete(0, END)
    for s in students:
        listbox_stud.insert(END, f"{s.name} {s.surname} ({s.group})")

def show_students_by_group():
    clear_all_markers()
    selected = entry_group_filter.get()
    listbox_stud.delete(0, END)
    for s in students:
        if s.group == selected:
            listbox_stud.insert(END, f"{s.name} {s.surname} ({s.university})")
            s.marker = map_widget.set_marker(s.coordinates[0], s.coordinates[1], text=f"{s.name} {s.surname}")

def show_student_details():
    idx = listbox_stud.index(ACTIVE)
    s = students[idx]
    print(f"{s.name} {s.surname}, {s.university}, {s.group}, {s.city}, {s.dormitory}")
def edit_student():
    idx = listbox_stud.index(ACTIVE)
    s = students[idx]
    entry_stud_name.insert(0, s.name)
    entry_stud_surname.insert(0, s.surname)
    entry_stud_university.insert(0, s.university)
    entry_stud_group.insert(0, s.group)
    entry_stud_city.insert(0, s.city)
    entry_stud_dormitory.insert(0, s.dormitory)
    btn_add_stud.configure(text="Zapisz", command=lambda: update_student(idx))

def update_student(idx):
    s = students[idx]
    s.marker.delete()
    s.name = entry_stud_name.get()
    s.surname = entry_stud_surname.get()
    s.university = entry_stud_university.get()
    s.group = entry_stud_group.get()
    s.city = entry_stud_city.get()
    s.dormitory = entry_stud_dormitory.get()
    s.coordinates = s.get_coordinates()
    s.marker = map_widget.set_marker(s.coordinates[0], s.coordinates[1], text=f"{s.name} {s.surname}")
    btn_add_stud.configure(text="Dodaj", command=add_student)
    clear_entries_stud()
    show_students()

def delete_student():
    idx = listbox_stud.index(ACTIVE)
    students[idx].marker.delete()
    students.pop(idx)
    show_students()

def clear_entries_stud():
    entry_stud_name.delete(0, END)
    entry_stud_surname.delete(0, END)
    entry_stud_university.delete(0, END)
    entry_stud_group.delete(0, END)
    entry_stud_city.delete(0, END)
    entry_stud_dormitory.delete(0, END)

Label(frame_stud, text="Imię:").grid(row=0, column=0)
entry_stud_name.grid(row=0, column=1)
Label(frame_stud, text="Nazwisko:").grid(row=1, column=0)
entry_stud_surname.grid(row=1, column=1)
Label(frame_stud, text="Uczelnia:").grid(row=2, column=0)
entry_stud_university.grid(row=2, column=1)
Label(frame_stud, text="Grupa:").grid(row=3, column=0)
entry_stud_group.grid(row=3, column=1)
Label(frame_stud, text="Miasto:").grid(row=4, column=0)
entry_stud_city.grid(row=4, column=1)
Label(frame_stud, text="Akademik:").grid(row=5, column=0)
entry_stud_dormitory = Entry(frame_stud)
entry_stud_dormitory.grid(row=5, column=1)

btn_add_stud = Button(frame_stud, text="Dodaj", command=add_student)
btn_add_stud.grid(row=7, column=1, columnspan=2)
Label(frame_stud, text="Filtruj grupę:").grid(row=6, column=0)
entry_group_filter.grid(row=6, column=1)
Button(frame_stud, text="Pokaż", command=show_students_by_group).grid(row=7, column=0, columnspan=2)
listbox_stud.grid(row=8, column=0, columnspan=2)
Button(frame_stud, text="Szczegóły", command=show_student_details).grid(row=9, column=0)
Button(frame_stud, text="Edytuj", command=edit_student).grid(row=9, column=1)
Button(frame_stud, text="Usuń", command=delete_student).grid(row=9, column=2)

root.mainloop()
