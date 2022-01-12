# Jugend forscht 2021 - Kevin Kretz, German Esaulkov, Leander Schäfer
import os
import xml.etree.ElementTree as ET

import requests

input_directory = "Input smi-files/"


def main():                                             # ! Hauptfunktion
    for smi_filename in os.listdir(input_directory):    # Für jede SMI-Datei im Inputverzeichnis wird Folgendes getan:
        smi_path = input_directory + smi_filename       # Der Name der Krankheit wird eingelesen.
        disease_name = smi_filename.rsplit(".")[0]
        disease_dir = disease_name + "/"
        if not os.path.exists(disease_dir):
            os.makedirs(disease_dir)
        print(disease_name)
        run_for_disease(smi_path, disease_dir)          # Die Funktion run_for_disease wird für die Krankheit ausgeführt.
        print("*****\n\n")


def read_in_strings(filename):
    file = open(filename)
    list_txt = file.readlines()

    strings = list(one_strings.rsplit("\t") for one_strings in list_txt)

    return strings


def substructure_search(strings_data, directory):
    strings_input = strings_data[0]
    ChEMBL_id_input = strings_data[1][:-1]

    substructure_results_request = requests.get('https://www.ebi.ac.uk/chembl/api/data/substructure/' + strings_input)
    substructure_results = substructure_results_request.content.decode()

    filename = "substructure_results_" + ChEMBL_id_input + ".xml"
    filepath = directory + filename

    xml_file = open(filepath, "w")
    xml_file.write(substructure_results)
    xml_file.close()

    tree = ET.parse(filepath)

    # tree = ET.fromstring(substructure_results)
    root = tree.getroot()

    for molecule in root.iter("molecule"):
        for molecule_chembl_id_ in molecule.iter("molecule_chembl_id"):
            molecule_chembl_id = molecule_chembl_id_.text
        for max_phase_ in molecule.iter("max_phase"):
            if max_phase_.text:
                max_phase = int(max_phase_.text)
                print("FOUND:     " + molecule_chembl_id + "\nFROM:      " + ChEMBL_id_input + "\nmax_phase: " + str(
                    max_phase))
            else:
                max_phase = -1


def run_for_disease(smi_path, disease_dir):         # !
    strings = read_in_strings(smi_path)

    for string in strings:
        substructure_search(string, disease_dir)


main()

# molecules_raw = substructure_results.rsplit("<molecules>")[1].rsplit("</molecules>")[0]
# molecules_list = list(molecule for molecule in molecules_raw.split("</molecule>"))

# for i in molecules_list:
#    print(i)
# print(molecules_list)
