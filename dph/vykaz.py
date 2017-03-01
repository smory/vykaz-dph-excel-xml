#!/usr/local/bin/python2.7
# encoding: utf-8

import xml.etree.ElementTree as ET;
import xml.dom.minidom as minidom;
import datetime;


baseXMLFilePath = "zaklad.xml";
baseCSVFilePath = "2017_01.csv";
outputXmlFilePath = "2017_01.xml";
nameSpace = {"ns0" : "https://ekr.financnasprava.sk/Formulare/XSD/kv_dph_2014.xsd"};


class Vykaz:
    
    TrElementName = "Transakcie";
    B1ElementName = "B1";
    B2ElementName = "B2";
    B3ElementName = "B3";
    
    sadzbaTag="S";
    odpocetTag = "O";
    danTag = "D";
    zakladTag = "Z";
    denTag = "Den";
    fakturaTag = "F";
    dodavatelTag = "Dod";
    
    def __init__(self, baseXMLPath):
        self.baseXMLPath = baseXMLPath;
        self.tree = ET.parse(baseXMLFilePath);
        self.root = self.tree.getroot();
        self.trElement = self.root.find( self.TrElementName);
    
    
    
    def addB1(self, odpocet="", sadzba="20", dan="", zaklad="", den="", faktura="", dodavatel=""):
        b1 = ET.Element(self.B1ElementName);
        b1.set(self.odpocetTag, str(odpocet));
        b1.set(self.sadzbaTag, str(sadzba));
        b1.set(self.danTag, str(dan));
        b1.set(self.zakladTag, str(zaklad));
        b1.set(self.denTag, str(den));
        b1.set(self.fakturaTag, str(faktura));
        b1.set(self.dodavatelTag, str(dodavatel));
        self.trElement.append(b1),
        
    def addB2(self, odpocet="", sadzba="20", dan="", zaklad="", den="", faktura="", dodavatel=""):
        b1 = ET.Element(self.B2ElementName);
        b1.set(self.odpocetTag, str(odpocet));
        b1.set(self.sadzbaTag, str(sadzba));
        b1.set(self.danTag, str(dan));
        b1.set(self.zakladTag, str(zaklad));
        b1.set(self.denTag, str(den));
        b1.set(self.fakturaTag, str(faktura));
        b1.set(self.dodavatelTag, str(dodavatel));
        self.trElement.append(b1),
    
    
    
    def addB3(self, odpocet="", dan="", zaklad=""):
        b3 = ET.Element(self.B3ElementName);
        b3.set(self.odpocetTag, str(odpocet));
        b3.set(self.danTag, str(dan));
        b3.set(self.zakladTag, str(zaklad));
        self.trElement.append(b3),
        
    def toString(self, prettyPrint = False):    
        rough_string = ET.tostring(self.root, 'utf-8');
        if prettyPrint:
            reparsed = minidom.parseString(rough_string);
            return reparsed.toprettyxml(indent="\t");
        else:
            return rough_string;
    
    
        
    def write(self, file):
        self.tree.write(file, "UTF-8", True);


class Faktura:
    
    def __init__(self, zaklad, dan, odpocet, den, dodavatel, faktura, sadzba = "20"):
        self.zaklad = zaklad;
        self.sadzba = sadzba;
        self.dan = dan;
        self.odpocet = odpocet;
        self.den = den;
        self.dodavatel = dodavatel;
        self.faktura = faktura;
        
    def __str__(self):
        return "IC dph = " + self.dodavatel + ", cislo = " + self.faktura + ", suma bez dph = " + self.zaklad + ", datum = " + self.den;
        
class Blocek:
     
    def __init__(self, zaklad, dan, odpocet):
        self.zaklad = zaklad;
        self.dan = dan;
        self.odpocet = odpocet;   
        
def readFileLines(fileName):
    lines = [line.strip() for line in open(fileName)];
    return lines;

def pridajFaktury(faktury, vykaz):
    for faktura in faktury:
        vykaz.addB2(odpocet = faktura.odpocet, dan = faktura.dan, zaklad = faktura.zaklad, den = faktura.den,
                    dodavatel = faktura.dodavatel, faktura = faktura.faktura);
        
def vytvorFaktury(riadky):
    
    i = 0;
    faktury = [];
    
    for riadok in riadky:
        i = i + 1;
        print(str(i));
        try:        
            strings = riadok.split(";");
            #print(str(strings));
            da = strings[3].split(".");
            print(str(da))
            datum = datetime.date(int(da[2]), int(da[1]), int(da[0]));
            #print(datum.isoformat());
            fa = Faktura(zaklad = strings[6], dan = strings[7], den = datum.isoformat(), dodavatel = strings[12], faktura = strings[2].replace(" " , ""),
                         odpocet = strings[7] );
            faktury.append(fa);
            print(str(fa));
        except:
            print("Chyba");
    return faktury;
        
    
    

riadky = readFileLines(baseCSVFilePath);
#print(str(riadky));
faktury = vytvorFaktury(riadky);

v = Vykaz(baseXMLFilePath);
#v.addB1("12", "20", "12.6", 100, "2014-6-4", "6942", "156948864");
#v.addB1("152", "20", "42.3", 200, "2014-8-5", "62", "156948864");
#v.addB3("0", 10, 50);
#print(v.toString());
pridajFaktury(faktury, v);
v.write(outputXmlFilePath);
