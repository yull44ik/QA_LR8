from parser import parse_iperf_output

class TestSuite:
    def test_iperf_client_connection(self, client):
        """
        Verifies iperf client's output to ensure traffic statistics meet expectations.
        """
        stdout, stderr = client
        assert not stderr, f"Client encountered an error: {stderr}"
        parsed_data = parse_iperf_output(stdout)
        
        # Verify traffic statistics
        for data in parsed_data:
            transfer_value, transfer_unit = data["Transfer"].split()
            bitrate_value, bitrate_unit = data["Bitrate"].split()
            
            # Convert values to float
            transfer = float(transfer_value)
            bitrate = float(bitrate_value)
            
            # Ensure correct units (e.g., GBytes, Mbits/sec)
            assert "Bytes" in transfer_unit, f"Unexpected transfer unit: {transfer_unit}"
            assert "bits/sec" in bitrate_unit, f"Unexpected bitrate unit: {bitrate_unit}"
            
            # Perform checks
            assert transfer > 2, f"Transfer is less than 2 {transfer_unit}"
            assert bitrate > 20, f"Bitrate is less than 20 {bitrate_unit}"

