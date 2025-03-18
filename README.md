# HtmlClonesDetector

## Descriere

HtmlClonesDetector este un program care, prin mai multe etape complexe, verifica similaritatea dintre mai multe website-uri!  
Logica de la baza este una foarte interesanta:

### Etapa 1: Verificarea codului HTML si CSS

- Ca prima etapa, am decis ca ar fi cel mai ok sa verific mai intai similaritatea dintre codul HTML prin libraria **html_similarity**.
- Aceasta librarie compara doua secvente in paralel, gaseste cea mai lunga subsecventa comuna si apeleaza recursiv pe celelalte ramase.
- Practic, verifica structura **HTML** si **CSS**.

### Etapa 2: Compararea vizuala a website-urilor

Verificarea codului HTML nu este suficienta, deoarece un website poate arata la fel pentru un utilizator, dar poate fi codat in mai multe feluri.  
Asadar, am decis ca cel mai bine este sa verificam aspectul propriu-zis.  

Ideea principala a fost sa fac **screenshots** la website-uri, apoi sa le compar pentru a determina similaritatea acestora.  
Am folosit doua metode:

#### **1. `compare_images_ssim`** (mai putin precisa, dar utila ca indicator)

- Am citit imaginile prin `cv2`.
- Am ales una dintre ele si i-am dat resize pentru a putea compara fara pierderi.
- Am impartit imaginile in canale **RGB** (puteam sa le transform in grayscale, dar am decis sa le las colorate).
- Am calculat pe rand **SSIM** pentru fiecare canal de culoare RGB pentru a verifica similaritatea.
- In final, am facut media acestora cu ajutorul librariei NumPy (`np.mean`).

#### **2. `calculate_feature_similarity`** (metoda precisa)

- Aici folosesc ca **base_model** `VGG16` - un model pre-antrenat de retea neuronala, antrenat pe ImageNet pentru a recunoaste diverse obiecte.
- Am folosit **block5_pool**, o matrice de trasaturi care reprezinta caracteristicile de inalt nivel ale imaginilor (forme, texturi, pattern-uri).

##### `preprocess_image` - Procesarea imaginilor

- Transform size-ul la **224x224** (acesta este input-ul acceptat de `VGG16`).
- Incarc imaginea intr-un array 3D (`224x224x3`).
- Aplic `expand_dims` pentru a crea un **batch** de imagini (`1x224x224x3`).
- Procesez imaginile cu `preprocess_input`.
- Folosesc `model.predict` pentru a extrage trasaturile vizuale.  
  - Output-ul produs de stratul `block5_pool` este de dimensiunea **`1x7x7x512`**.
  - `1` - lotul de imagini, `7x7` - dimensiunea imaginii in spatiul caracteristicilor, `512` - numarul de canale de trasaturi extrase.
  - Aplic `.flatten()` pentru a transforma matricea 4D intr-un vector 1D.
- Calculez **similaritatea cosinus** intre vectorii unidimensionali si returnez rezultatul.

---

## Logica principala (`check_all`)

- Pas cu pas, verific un website cu celelalte din vectorul meu de site-uri.
- Daca similaritatea este mare, le adaug in aceeasi lista si le sterg din lista principala.
- Parcurg recursiv tot array-ul pana cand acesta ramane gol.
- Mai intai creez lista `onlyfiles`, apoi apelez `check_all`.
- La final, adaug toate listele intr-o lista principala si afisez rezultatul.
- Sterg toate imaginile salvate in **`images/`**.

- PS : toate functiile care calculeaza similarity returneaza un numar intre 0 si 1 (care indica cat de similare sunt acestea) 
---

## Observatii

 **Timp de executie**:  
- Poate rula mai mult timp, deoarece procesul de `take_screenshot` este costisitor.  
- In rest, toate celelalte etape se executa rapid fara probleme.  

---