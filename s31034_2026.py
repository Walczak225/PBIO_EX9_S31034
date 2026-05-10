#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random


def generate_sequence(length):
    dna = ""
    for i in range(length):
        los = random.randint(1, 4)
        if los == 1:
            dna = dna + "A"
        elif los == 2:
            dna = dna + "C"
        elif los == 3:
            dna = dna + "G"
        else:
            dna = dna + "T"
    return dna


def calculate_stats(sequence):
    a = 0
    c = 0
    g = 0
    t = 0

    for znak in sequence:
        if znak == "A":
            a = a + 1
        elif znak == "C":
            c = c + 1
        elif znak == "G":
            g = g + 1
        elif znak == "T":
            t = t + 1

    dlugosc = len(sequence)
    procent_a = (a / dlugosc) * 100
    procent_c = (c / dlugosc) * 100
    procent_g = (g / dlugosc) * 100
    procent_t = (t / dlugosc) * 100
    gc = ((g + c) / dlugosc) * 100

    stats = {"A": procent_a, "C": procent_c, "G": procent_g, "T": procent_t, "GC": gc}
    return stats


def insert_name(sequence, name):
    imie = name.lower()
    if len(sequence) == 0:
        return imie

    pozycja = random.randint(0, len(sequence))

    nowy = sequence[:pozycja] + imie + sequence[pozycja:]
    return nowy


def format_fasta(seq_id, description, sequence, line_width=80):
    naglowek = ">" + seq_id
    if description != "":
        naglowek = naglowek + " " + description

    wynik = naglowek + "\n"

    i = 0
    while i < len(sequence):
        koniec = i + line_width
        if koniec > len(sequence):
            koniec = len(sequence)
        wynik = wynik + sequence[i:koniec] + "\n"
        i = i + line_width

    return wynik


def validate_positive_int(prompt, min_val=1, max_val=100000):
    while True:
        tekst = input(prompt)
        try:
            liczba = int(tekst)
            if liczba >= min_val and liczba <= max_val:
                return liczba
            else:
                print("Error: value must be an integer in the range [" + str(min_val) + ", " + str(max_val) + "].")
        except:
            print("Error: value must be an integer in the range [" + str(min_val) + ", " + str(max_val) + "].")


def validate_id(prompt):
    while True:
        identyfikator = input(prompt)
        identyfikator = identyfikator.strip()
        if identyfikator != "" and " " not in identyfikator:
            return identyfikator
        print("Error: ID cannot contain whitespace and cannot be empty.")

def batch_mode():
    liczba = validate_positive_int("Enter number of sequences to generate: ", 1, 1000)
    dlugosc = validate_positive_int("Enter sequence length for each: ", 1, 100000)

    opis = input("Enter description for all sequences: ").strip()
    imie = input("Enter your name: ").strip()
    while imie == "":
        imie = input("Enter your name: ").strip()

    nazwa_pliku = input("Enter output filename: ").strip()
    if nazwa_pliku == "":
        nazwa_pliku = "batch.fasta"

    plik = open(nazwa_pliku, "w")

    for i in range(1, liczba + 1):
        id_sekwencji = "Seq_" + str(i).zfill(3)
        sekwencja = generate_sequence(dlugosc)
        sekwencja_z_imieniem = insert_name(sekwencja, imie)

        wpis = format_fasta(id_sekwencji, opis, sekwencja_z_imieniem)
        plik.write(wpis)

        statystyki = calculate_stats(sekwencja)
        print("\n--- " + id_sekwencji + " statistics (n=" + str(dlugosc) + ") ---")
        print("A: " + format(statystyki["A"], ".2f") + "%")
        print("C: " + format(statystyki["C"], ".2f") + "%")
        print("G: " + format(statystyki["G"], ".2f") + "%")
        print("T: " + format(statystyki["T"], ".2f") + "%")
        print("GC content: " + format(statystyki["GC"], ".2f") + "%")

    plik.close()
    print("\nAll sequences saved to: " + nazwa_pliku)


def motif_search():
    dlugosc = validate_positive_int("Enter sequence length: ")
    id_sekwencji = validate_id("Enter sequence ID: ")
    opis = input("Enter description: ").strip()
    imie = input("Enter your name: ").strip()
    while imie == "":
        imie = input("Enter your name: ").strip()

    sekwencja = generate_sequence(dlugosc)
    sekwencja = insert_name(sekwencja, imie)

    motyw = input("Enter motif to search: ").upper().strip()

    pozycje = []
    for i in range(len(sekwencja) - len(motyw) + 1):
        fragment = sekwencja[i:i + len(motyw)]
        if fragment == motyw:
            pozycje.append(i + 1)

    statystyki = calculate_stats(sekwencja)
    print("\nSequence statistics (n=" + str(dlugosc) + "):")
    print("A: " + format(statystyki["A"], ".2f") + "%")
    print("C: " + format(statystyki["C"], ".2f") + "%")
    print("G: " + format(statystyki["G"], ".2f") + "%")
    print("T: " + format(statystyki["T"], ".2f") + "%")
    print("GC content: " + format(statystyki["GC"], ".2f") + "%")

    if len(pozycje) > 0:
        print("\nMotif '" + motyw + "' found at positions: " + str(pozycje))
    else:
        print("\nMotif '" + motyw + "' not found.")

    nazwa_pliku = id_sekwencji + ".fasta"
    plik = open(nazwa_pliku, "w")
    plik.write(format_fasta(id_sekwencji, opis, sekwencja))
    plik.close()
    print("\nSequence saved to: " + nazwa_pliku)


def complement_and_reverse():
    dlugosc = validate_positive_int("Enter sequence length: ")
    id_sekwencji = validate_id("Enter sequence ID: ")
    opis = input("Enter description: ").strip()
    imie = input("Enter your name: ").strip()
    while imie == "":
        imie = input("Enter your name: ").strip()

    sekwencja = generate_sequence(dlugosc)
    sekwencja = insert_name(sekwencja, imie)

    komplementarna = ""
    for znak in sekwencja:
        if znak == "A":
            komplementarna = komplementarna + "T"
        elif znak == "T":
            komplementarna = komplementarna + "A"
        elif znak == "C":
            komplementarna = komplementarna + "G"
        elif znak == "G":
            komplementarna = komplementarna + "G"
        else:
            komplementarna = komplementarna + znak

    odwrotna = ""
    for i in range(len(komplementarna) - 1, -1, -1):
        odwrotna = odwrotna + komplementarna[i]

    statystyki = calculate_stats(sekwencja)
    print("\nSequence statistics (n=" + str(dlugosc) + "):")
    print("A: " + format(statystyki["A"], ".2f") + "%")
    print("C: " + format(statystyki["C"], ".2f") + "%")
    print("G: " + format(statystyki["G"], ".2f") + "%")
    print("T: " + format(statystyki["T"], ".2f") + "%")
    print("GC content: " + format(statystyki["GC"], ".2f") + "%")

    nazwa_pliku = id_sekwencji + "_complements.fasta"
    plik = open(nazwa_pliku, "w")
    plik.write(format_fasta(id_sekwencji, opis, sekwencja))
    plik.write(format_fasta(id_sekwencji + "_complement", "Complement", komplementarna))
    plik.write(format_fasta(id_sekwencji + "_reverse", "Reverse complement", odwrotna))
    plik.close()

    print("\nSequences saved to: " + nazwa_pliku)


def transcription():
    dlugosc = validate_positive_int("Enter sequence length: ")
    id_sekwencji = validate_id("Enter sequence ID: ")
    opis = input("Enter description: ").strip()
    imie = input("Enter your name: ").strip()
    while imie == "":
        imie = input("Enter your name: ").strip()

    sekwencja = generate_sequence(dlugosc)
    sekwencja = insert_name(sekwencja, imie)

    mrna = ""
    for znak in sekwencja:
        if znak == "T":
            mrna = mrna + "U"
        else:
            mrna = mrna + znak

    statystyki = calculate_stats(sekwencja)
    print("\nSequence statistics (n=" + str(dlugosc) + "):")
    print("A: " + format(statystyki["A"], ".2f") + "%")
    print("C: " + format(statystyki["C"], ".2f") + "%")
    print("G: " + format(statystyki["G"], ".2f") + "%")
    print("T: " + format(statystyki["T"], ".2f") + "%")
    print("GC content: " + format(statystyki["GC"], ".2f") + "%")

    nazwa_pliku = id_sekwencji + "_mrna.fasta"
    plik = open(nazwa_pliku, "w")
    plik.write(format_fasta(id_sekwencji, opis, sekwencja))
    plik.write(format_fasta(id_sekwencji + "_mRNA", "Transcribed mRNA", mrna))
    plik.close()

    print("\nDNA and mRNA saved to: " + nazwa_pliku)


def main():
    print("=== DNA Sequence Generator ===\n")
    print("Choose mode:")
    print("1. Single sequence (basic)")
    print("2. Batch mode (multiple sequences)")
    print("3. Motif search")
    print("4. Complement & reverse complement")
    print("5. Transcription DNA -> mRNA")

    wybor = input("\nEnter your choice (1-5): ")

    if wybor == "1":
        dlugosc = validate_positive_int("Enter sequence length: ")
        id_sekwencji = validate_id("Enter sequence ID: ")
        opis = input("Enter description of the sequence: ").strip()
        imie = input("Enter your name: ").strip()
        while imie == "":
            imie = input("Enter your name: ").strip()

        sekwencja = generate_sequence(dlugosc)
        sekwencja_z_imieniem = insert_name(sekwencja, imie)

        nazwa_pliku = id_sekwencji + ".fasta"
        plik = open(nazwa_pliku, "w")
        plik.write(format_fasta(id_sekwencji, opis, sekwencja_z_imieniem))
        plik.close()

        statystyki = calculate_stats(sekwencja)
        print("\nSequence saved to file: " + nazwa_pliku)
        print("\nSequence statistics (n=" + str(dlugosc) + "):")
        print("A: " + format(statystyki["A"], ".2f") + "%")
        print("C: " + format(statystyki["C"], ".2f") + "%")
        print("G: " + format(statystyki["G"], ".2f") + "%")
        print("T: " + format(statystyki["T"], ".2f") + "%")
        print("GC content: " + format(statystyki["GC"], ".2f") + "%")

    elif wybor == "2":
        batch_mode()
    elif wybor == "3":
        motif_search()
    elif wybor == "4":
        complement_and_reverse()
    elif wybor == "5":
        transcription()
    else:
        print("Invalid choice. Run again and select 1-5.")


if __name__ == "__main__":
    main()