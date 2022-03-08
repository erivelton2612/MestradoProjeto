import time, itertools
import sys
import os

#def obter_agenda(data: str) -> List[Dict]:
#    req = requests.get(
#        url="https://app.sinconecta.com/ords/saude/TuoTempo/getAppointments",
#        headers={"START_DATE": data, "END_DATE": data},
#        auth=(os.environ["SINCONECTA_API_USUARIO"], os.environ["SINCONECTA_API_SENHA"]),
#        verify=False,
#    ).json()

#    consultas = req["items"]
#    return consultas



#CAPACIDADE
path = os.getcwd()+"\\data\\class6\\cap\\6AA1_11.cap"
t = 30
rec = 11
cap = 12


f = open(path, "w")

for nt in range(t):
    for nrec in range(rec):
        f.write(str(nt +1) + "\t" + str(nrec +1) + "\t" + str(cap)+ "\n")

f.write("#1 resource number\n#2 period number\n#3 capacity")