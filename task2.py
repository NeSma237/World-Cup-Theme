class TicketCodec:

    def calculate_checksum(self, ticket_id):
        # Implement checksum calculation logic here
        checksum = sum(ord(char) * (i + 1) for i, char in enumerate(ticket_id)) % 256
        return checksum

    def encode(self, ticket_id):
        # Implement encoding logic here
        checksum = self.calculate_checksum(ticket_id)
        return ticket_id + f"{checksum:02x}"

    def decode(self, barcode):
        # Implement decoding logic here
        ticket = barcode[:-2]
        checksum = int(barcode[-2:], 16)  # el qema el checksum elly et7sb mn el ticket
        checksum_calculated = self.calculate_checksum(barcode[:-2])  # el qema elly et7sb mn el ticket
        if checksum == checksum_calculated:
            return ticket
        else:
            print(f"Checksum mismatch: expected {checksum_calculated}, got {checksum}")
            return "CORRUPTED TICKET: Checksum does not match."
        

if __name__ == "__main__":
    codec = TicketCodec()

    # Example usage
    ticket_id = "TICKET123"
    encoded_ticket = codec.encode(ticket_id)
    print(f"Encoded ticket: {encoded_ticket}")

    decoded_ticket = codec.decode(encoded_ticket)
    print(f"Decoded ticket: {decoded_ticket}")

    # Test with a corrupted ticket
    corrupted_ticket = encoded_ticket[:-2] + "ff"  # Change the checksum to an incorrect value
    decoded_corrupted_ticket = codec.decode(corrupted_ticket)
    print(f"Decoded corrupted ticket: {decoded_corrupted_ticket}")

    corrupted_ticket = "X" + encoded_ticket[1:]  
    decoded_corrupted_ticket = codec.decode(corrupted_ticket)
    print(f"Decoded corrupted ticket: {decoded_corrupted_ticket}")

    ticket_id2 = "GATE2026A"
    encoded_ticket2 = codec.encode(ticket_id2)
    print(f"Encoded ticket: {encoded_ticket2}")

    decoded_ticket2 = codec.decode(encoded_ticket2)
    print(f"Decoded ticket: {decoded_ticket2}")

    ticket_id2 = "ticket2026B"
    encoded_ticket2 = codec.encode(ticket_id2)
    print(f"Encoded ticket: {encoded_ticket2}")

    decoded_ticket2 = codec.decode(encoded_ticket2)
    print(f"Decoded ticket: {decoded_ticket2}")