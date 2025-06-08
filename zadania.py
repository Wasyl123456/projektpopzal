from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

class University:
    def __init__(self, name, voivodeship, district):
        self.name = name
        self.voivodeship = voivodeship
        self.district = district
        self.coordinates = self.get_coordinates()

    def get_coordinates(self):
        address_url = f"https://pl.wikipedia.org/wiki/{self.name}"
        response = requests.get(address_url).text
        response_html = BeautifulSoup(response, "html.parser")
        lon = float(response_html.select(".longitude")[1].text.replace(",", "."))
        lat = float(response_html.select(".latitude")[1].text.replace(",", "."))
        return [lat, lon]

class Student:
    def __init__(self, name, surname, university, group):
        self.name = name
        self.surname = surname
        self.university = university
        self.group = group
        #self.coordinates = self.get_coordinates()

class Employee:
    def __init__(self, name, surname, university):
        self.name = name
        self.surname = surname
        self.university = university

universities = [University(name="Uniwersytet Warszawski", voivodeship="Mazowieckie", district="Warszawa")]
students = [Student(name="Łukasz", surname="Wasilewski", university="Uniwersytet Warszawski", group="wwa")]
employees = [Employee(name="Rafał", surname="Kowalski", university="Uniwersytet Warszawski")]

def add_university():
    name = entry_name.get()
    voiv = entry_voiv.get()
    dist = entry_dist.get()
    uni = University(name, voiv, dist)
    universities.append(uni)
    entry_name.delete(0, END)
    entry_voiv.delete(0, END)
    entry_dist.delete(0, END)
    entry_name.focus()
    show_universities()

def show_universities(filtered=None):
    listbox.delete(0, END)
    map_widget.set_position(52.23, 21)
    map_widget.set_zoom(6)
    map_widget.delete_all_marker()

    data = filtered if filtered is not None else universities
    for idx, uni in enumerate(data):
        listbox.insert(idx, f"{idx+1}. {uni.name}, {uni.voivodeship}, {uni.district}")
        map_widget.set_marker(uni.coordinates[0], uni.coordinates[1], text=uni.name)

def show_students(filtered=None):
    listbox_students.delete(0, END)
    map_widget.set_position(52.23, 21)
    map_widget.set_zoom(6)
    map_widget.delete_all_marker()

    data = filtered if filtered is not None else students
    for idx, stu in enumerate(data):
        listbox_students.insert(idx, f"{idx+1}. {stu.name}, {stu.surname}, {stu.university}, {stu.group}")

def show_employees(filtered=None):
    listbox_employee.delete(0, END)
    map_widget.set_position(52.23, 21)
    map_widget.set_zoom(6)
    map_widget.delete_all_marker()

    data = filtered if filtered is not None else employees
    for idx, emp in enumerate(data):
        listbox_employee.insert(idx, f"{idx+1}. {emp.name}, {emp.surname}, {emp.university},")

def delete_university():
    idx = listbox.index(ACTIVE)
    universities.pop(idx)
    show_universities()

def delete_student():
    idx = listbox.index(ACTIVE)
    students.pop(idx)
    show_students()

def delete_employee():
    idx = listbox.index(ACTIVE)
    employees.pop(idx)
    show_employees()

def filter_by_voivodeship():
    voiv = entry_filter_voiv.get().strip().lower()
    if voiv != "":
        filtered = [u for u in universities if u.voivodeship.lower() == voiv]
        show_universities(filtered)
    else:
        show_universities(universities)

# GUI
root = Tk()
root.title("Uczelnie - System Zarządzania")
root.geometry("1024x768")

# RAMKI
frame_form = Frame(root)
frame_form.grid(row=0, column=0, padx=10, pady=10, sticky=N)

frame_list = Frame(root)
frame_list.grid(row=0, column=1, padx=10, pady=10, sticky=N)

frame_map = Frame(root)
frame_map.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# FORMULARZ – LEWA STRONA
Label(frame_form, text="Nazwa uczelni:").grid(row=0, column=0, sticky=W)
entry_name = Entry(frame_form, width=30)
entry_name.grid(row=0, column=1)

Label(frame_form, text="Województwo:").grid(row=1, column=0, sticky=W)
entry_voiv = Entry(frame_form, width=30)
entry_voiv.grid(row=1, column=1)

Label(frame_form, text="Powiat:").grid(row=2, column=0, sticky=W)
entry_dist = Entry(frame_form, width=30)
entry_dist.grid(row=2, column=1)

button_add = Button(frame_form, text="Dodaj uczelnię", width=25, command=add_university)
button_add.grid(row=3, column=0, columnspan=2, pady=10)

# LISTA + FILTR – PRAWA STRONA
Label(frame_list, text="Lista uczelni:").grid(row=0, column=0, sticky=W)
listbox = Listbox(frame_list, width=30)
listbox.grid(row=1, column=0)

Label(frame_list, text="Lista studentów:").grid(row=0, column=1, sticky=W)
listbox_students = Listbox(frame_list, width=30)
listbox_students.grid(row=1, column=1)

Label(frame_list, text="Lista pracowników:").grid(row=0, column=2, sticky=W)
listbox_employee = Listbox(frame_list, width=30)
listbox_employee.grid(row=1, column=2)

button_delete = Button(frame_list, text="Usuń uczelnię", width=25, command=delete_university)
button_delete.grid(row=2, column=0, pady=5)

button_delete = Button(frame_list, text="Usuń studenta", width=25, command=delete_student)
button_delete.grid(row=2, column=1, pady=5)

button_delete = Button(frame_list, text="Usuń pracownika", width=25, command=delete_employee)
button_delete.grid(row=2, column=2, pady=5)

Label(frame_list, text="Filtruj po województwie:").grid(row=3, column=0, sticky=W, pady=(10,0))
entry_filter_voiv = Entry(frame_list, width=30)
entry_filter_voiv.grid(row=4, column=0)

button_filter = Button(frame_list, text="Filtruj", width=25, command=filter_by_voivodeship)
button_filter.grid(row=5, column=0, pady=5)

# MAPA – DÓŁ
map_widget = tkintermapview.TkinterMapView(frame_map, width=1024, height=400)
map_widget.set_position(52.23, 21)
map_widget.set_zoom(6)
map_widget.grid(row=0, column=0)

show_students()
show_universities()
show_employees()

root.mainloop()