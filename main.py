import os
import requests
import xml.etree.ElementTree as ET
import json

input_directory = "Input smi-files/"
output = open("output.json", "w")


def main():  # Hauptfunktion: Ruft andere Funktionen auf.
    everything = {}
    for smi_filename in os.listdir(input_directory):  # Für jede SMI-Datei im Inputverzeichnis wird Folgendes getan:
        smi_path = input_directory + smi_filename
        disease_name = smi_filename.rsplit(".")[0]  # Der Name der Krankheit wird eingelesen.
        disease_dir = disease_name + "/"
        if not os.path.exists(disease_dir):
            os.makedirs(disease_dir)
        print(disease_name)
        results_of_disease = run_for_disease(smi_path,
                                             disease_dir)  # Die Funktion run_for_disease wird für die Krankheit ausgeführt.
        print(make_look_good(results_of_disease))
        everything.update({disease_name: results_of_disease})

    json.dump(everything, output)


def make_look_good(results):  # Bereitet die Ergebnisse übersichtlich auf.
    out = ""
    for mol in results:
        out += "Original:  " + mol + "\n"
        for sim in results[mol]:
            out += "Similar:   " + sim + "\n"
            out += "max_phase: " + str(results[mol][sim]["max_phase"]) + "\n"
    return out


def read_in_strings(filename):  # Liest eine SMI-Datei und bereitet die Daten auf.
    file = open(filename)
    list_txt = file.readlines()

    strings = list(one_strings.rsplit("\t") for one_strings in list_txt)

    return strings


def substructure_search(strings, filepath):  # Stellt die Substructure-Suchanfrage an die ChEMBL-API
    substructure_results_request = requests.get('https://www.ebi.ac.uk/chembl/api/data/substructure/' + strings)
    substructure_results = substructure_results_request.content.decode()

    return substructure_results


def store_file(data, filepath):  # Speichert Daten.
    file = open(filepath, "w")
    file.write(data)
    file.close()


def make_file_path(directory, chembl_id):  # Erstellt den Pfad zur Antwort einer ChEMBL-Anfrage.
    filename = "substructure_results_" + chembl_id + ".xml"
    filepath = directory + filename
    return filepath


def get_max_phase(filepath_of_response):  # Liest max_phase aus ChEMBL-Antwort aus.
    tree = ET.parse(filepath_of_response)
    root = tree.getroot()

    found = {}

    for molecule in root.iter("molecule"):
        max_phase = False
        for molecule_chembl_id_ in molecule.iter("molecule_chembl_id"):
            molecule_chembl_id = molecule_chembl_id_.text
        for max_phase_ in molecule.iter("max_phase"):
            if max_phase_.text:
                max_phase = int(max_phase_.text)

        if max_phase:
            found.update({molecule_chembl_id: {"max_phase": int(max_phase)}})

    return found


def run_for_disease(smi_path, disease_dir):  # Ruft die notwendigen Funktionen auf, um eine SMI-Datei abzuarbeiten.
    strings = read_in_strings(smi_path)
    disease_found = {}

    for string in strings:
        strings_input = string[0]
        chembl_id_input = string[1][:-1]

        filepath = make_file_path(disease_dir, chembl_id_input)
        substructure_results = substructure_search(strings_input, filepath)
        store_file(substructure_results, filepath)
        found = get_max_phase(filepath)

        if len(found):
            disease_found.update({chembl_id_input: found})

    return disease_found


main()
