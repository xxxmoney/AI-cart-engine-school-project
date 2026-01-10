# **Shrnutí školního projektu: Trénování AI autíčka**

Tento projekt je soutěžní úloha, kde je cílem naprogramovat a natrénovat umělou inteligenci (agenta), která dokáže samostatně, rychle a bezpečně projet závodní trať v simulovaném 2D prostředí.

### **1\. Hlavní cíl**

* **Navrhnout "mozek" (AI agenta):** Vytvořit třídu v Pythonu, která na základě vstupů ze senzorů (vzdálenost od překážek) rozhoduje o akcích auta (plyn, brzda, zatáčení).  
* **Natrénovat agenta:** Použít **evoluční algoritmy** (nikoliv klasické učení s učitelem), kdy se agent učí systémem pokus-omyl, selekcí nejlepších jedinců a jejich mutací.

### **2\. Princip fungování**

* **Vstupy (Senzory):** Agent dostává informace z "raycastů" (paprsků), které měří vzdálenost k okraji tratě nebo překážkám.  
* **Výstupy (Akce):** Agent vrací 4 hodnoty, které reprezentují akce:  
  * 0: Dopředu (plyn)  
  * 1: Dozadu (brzda/zpátečka)  
  * 2: Doleva  
  * 3: Doprava.  
* **Učení:** Probíhá v cyklech (generacích). V každé generaci soutěží populace aut. Ta s nejlepším "fitness" (skóre založené na vzdálenosti, čase, atd.) přežijí a jejich parametry se s drobnými změnami (mutacemi) přenesou do další generace.

### **3\. Technické zadání a omezení**

* **Jazyk:** Python (vyžaduje se verze 3.12+).  
* **Povolené úpravy:** Smíš vytvořit **pouze** nový soubor AI\_engines/AIbrain\_\<Tym\>.py a upravit jeden import v main.py. Zbytek kódu (fyzika, grafika, engine) se nesmí měnit.  
* **Odevzdání:**  
  1. Zdrojový kód mozku: AIbrain\_\<Tym\>.py.  
  2. Soubor s natrénovanými parametry: AIbrain\_\<Tym\>.npz.

### **4\. Hodnocení**

* 40 % Funkčnost a smysluplnost řešení.  
* 30 % Aktivita na workshopu.  
* 20 % Prezentace.  
* 10 % Schopnost projet tratě.