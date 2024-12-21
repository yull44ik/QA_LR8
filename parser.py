import re

# Regular expression to match iperf output for traffic data
REGEXP = r'\[\s*\d+\]\s+(\d+\.\d+-\d+\.\d+)\s+sec\s+(\d+\.\d+)\s+([A-Za-z]+Bytes)\s+(\d+\.\d+)\s+([A-Za-z]+bits/sec)'

def parse_iperf_output(output):
    """
    Parses the iperf client output to extract traffic statistics.
    """
    matches = re.findall(REGEXP, output)
    parsed_data = []
    for match in matches:
        interval, transfer, transfer_unit, bitrate, bitrate_unit = match
        parsed_data.append({
            "Interval": interval,
            "Transfer": f"{transfer} {transfer_unit}",
            "Bitrate": f"{bitrate} {bitrate_unit}"
        })
    return parsed_data

