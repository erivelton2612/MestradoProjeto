import time, itertools
import sys

def obter_agenda(data: str) -> List[Dict]:
    req = requests.get(
        url="https://app.sinconecta.com/ords/saude/TuoTempo/getAppointments",
        headers={"START_DATE": data, "END_DATE": data},
        auth=(os.environ["SINCONECTA_API_USUARIO"], os.environ["SINCONECTA_API_SENHA"]),
        verify=False,
    ).json()

    consultas = req["items"]
    return consultas