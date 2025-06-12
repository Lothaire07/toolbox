
import asyncio, csv
from pysnmp.hlapi.v3arch.asyncio import (
    get_cmd,
    SnmpEngine,
    CommunityData,
    ContextData,
    ObjectType,
    ObjectIdentity,
    UdpTransportTarget,
)

def load_ips_from_file(path="ip.txt") -> list[str]:
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

PRINTER_IPS = load_ips_from_file()
OID_BW = "1.3.6.1.4.1.2385.1.1.19.2.1.3.5.4.61"
OID_COLOR = "1.3.6.1.4.1.2385.1.1.19.2.1.3.5.4.63"
OID_NAME = "1.3.6.1.2.1.1.5.0"


# -----------  async utilitaire  --------------------------------------------
async def snmp_get(ip: str, oid: str, community="public") -> str | None:
    transport = await UdpTransportTarget.create(
        (ip, 161), timeout=4, retries=1
    )
    errInd, errStat, errIdx, varBinds = await get_cmd(
        SnmpEngine(),
        CommunityData(community),
        transport,
        ContextData(),
        ObjectType(ObjectIdentity(oid)),
    )
    if errInd or errStat:
        return None
    return str(varBinds[0][1])

def snmp_get_blocking(ip: str, oid: str, community="public") -> str | None:
    return asyncio.run(snmp_get(ip, oid, community))


def main() -> None:
    rows = []
    for ip in PRINTER_IPS:
        name = snmp_get_blocking(ip, OID_NAME) or "N/A"
        bw = snmp_get_blocking(ip, OID_BW) or "N/A"
        color = snmp_get_blocking(ip, OID_COLOR) or "N/A"
        rows.append({"IP": ip, "Nom": name, "Noir et Blanc": bw, "Couleur": color})

    with open("../../PycharmProjects/printer/compteurs_imprimantes.csv", "w", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=rows[0].keys(), delimiter=';').writeheader()
        csv.DictWriter(f, fieldnames=rows[0].keys(), delimiter=';').writerows(rows)

    print("Fichier CSV généré : compteurs_imprimantes.csv")


if __name__ == "__main__":
    main()
