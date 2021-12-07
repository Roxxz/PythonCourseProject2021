# PythonCourseProject2021

Scrieți un script care va primi ca parametru un URL ( un link către o pagina wikipedia ) și va

stoca pe disk în format JSON informații relevante găsite în pagina precum titlu, cuvantul care

apare de mai multe ori, src-urile tuturor imaginilor din pagina si imaginile salvate pe disk.

INPUT:

- URL ex: https://ro.wikipedia.org/wiki/Regnul_Fungi


OUTPUT: 

Un obiect in format JSON de ex:

{“title” : <title>,
  
“Most_frequent_word”: <word>,
  
“Images”: <list_src_img>”, 
  
}
