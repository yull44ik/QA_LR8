import subprocess

def client(server_ip):
    """
    Функція для підключення клієнта до iperf-сервера.

    :param server_ip: IP-адреса сервера
    :return: Вивід та помилка процесу
    """
    try:
        process = subprocess.Popen(
            ["iperf", "-c", server_ip, "-i", "1"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output, error = process.communicate()
        return output, error
    except Exception as e:
        return None, str(e)

def parse_iperf_output(output):
    """
    Функція для парсингу виводу iperf.

    :param output: Вивід команди iperf
    :return: Список інтервалів з деталями
    """
    import re
    pattern = r"(?P<Interval>\d+\.\d+-\d+\.\d+)\s+sec\s+(?P<Transfer>\d+\.\d+)\s+(?P<Unit>\w+)\s+(?P<Bitrate>\d+\.\d+)\s+(?P<BitrateUnit>\w+)"
    matches = re.finditer(pattern, output)
    results = []
    for match in matches:
        results.append({
            "Interval": match.group("Interval"),
            "Transfer": float(match.group("Transfer")),
            "Bitrate": float(match.group("Bitrate"))
        })
    return results

if __name__ == "__main__":
    server_ip = "127.0.0.1"  # Змініть на адресу сервера
    output, error = client(server_ip)

    if error:
        print("Error:", error)
    else:
        results = parse_iperf_output(output)
        for entry in results:
            if entry["Transfer"] > 2 and entry["Bitrate"] > 20:
                print(entry)
