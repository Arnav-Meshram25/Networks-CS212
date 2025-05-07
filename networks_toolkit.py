import os
import platform
import subprocess
import socket
import requests
import speedtest

def show_menu():
    print("\nSwiss Knife Network Tool (Windows Edition)")
    print("--------------------------------------------")
    print("1. Show Available Wi-Fi Networks")
    print("2. Internet Speed Test")
    print("3. IP Geolocation (Your Own IP)")
    print("4. IP Geolocation (Any IP)")
    print("5. Ping a Website/IP")
    print("6. Traceroute to Host/IP (with Configurations)")
    print("7. HTTP Server Header Grabber")
    print("8. Get External IP Address")
    print("9. DNS Lookup")
    print("10. Show User Manual")
    print("0. Exit")
    print("--------------------------------------------")

def show_manual():
    print("\nUSER MANUAL")
    print("--------------------------------------------")
    print("This tool offers essential network functions:")
    print("1 - List nearby Wi-Fi networks (Windows only)")
    print("2 - Test your internet download/upload speeds")
    print("3 - Show your IP geolocation (city, country, org)")
    print("4 - Get geolocation for any IP address")
    print("5 - Ping a domain or IP to check reachability")
    print("6 - Traceroute with optional settings:")
    print("    - Skip DNS resolution (-d)")
    print("    - Set max hops (-h)")
    print("    - Set timeout (-w, in ms)")
    print("7 - Fetch HTTP response headers from a website")
    print("8 - Get your external (public) IP address")
    print("9 - Perform DNS lookup on a domain")
    print("\nNote: Requires Windows system. Libraries needed:")
    print(" - requests")
    print(" - speedtest-cli")
    print("--------------------------------------------")

def wifi_networks():
    print("\nAvailable Wi-Fi Networks:")
    try:
        output = subprocess.check_output(['netsh', 'wlan', 'show', 'networks'], text=True, stderr=subprocess.STDOUT)
        print(output)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.output}")

def internet_speed_test():
    print("\nTesting Internet Speed...")
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000
        upload_speed = st.upload() / 1_000_000
        ping = st.results.ping
        print(f"Download Speed: {download_speed:.2f} Mbps")
        print(f"Upload Speed: {upload_speed:.2f} Mbps")
        print(f"Ping: {ping} ms")
    except Exception as e:
        print(f"Error during speed test: {e}")

def own_ip_geolocation():
    print("\nFetching Your IP Geolocation...")
    try:
        response = requests.get('https://ipinfo.io/json', timeout=5)
        data = response.json()
        print(f"IP: {data.get('ip')}")
        print(f"City: {data.get('city')}")
        print(f"Region: {data.get('region')}")
        print(f"Country: {data.get('country')}")
        print(f"Location (Lat,Long): {data.get('loc')}")
        print(f"Org: {data.get('org')}")
    except Exception as e:
        print(f"Error fetching geolocation: {e}")

def any_ip_geolocation():
    ip = input("Enter IP address to locate: ")
    print(f"\nFetching Geolocation for {ip}...")
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json', timeout=5)
        data = response.json()
        print(f"IP: {data.get('ip')}")
        print(f"City: {data.get('city')}")
        print(f"Region: {data.get('region')}")
        print(f"Country: {data.get('country')}")
        print(f"Location (Lat,Long): {data.get('loc')}")
        print(f"Org: {data.get('org')}")
    except Exception as e:
        print(f"Error fetching geolocation: {e}")

def ping_website():
    target = input("Enter domain or IP to ping: ")
    print(f"\nPinging {target}...")
    try:
        output = subprocess.check_output(["ping", target], text=True)
        print(output)
    except subprocess.CalledProcessError as e:
        print(f"Ping failed: {e.output}")

def traceroute():
    target = input("Enter domain or IP to traceroute: ")
    print("\nAvailable traceroute configurations:")
    print(" - Skip DNS resolution (-d)")
    print(" - Set maximum hops (-h, default 30)")
    print(" - Set timeout per hop (-w, default 4000 ms)")

    skip_dns_input = input("Skip DNS resolution? (y/n): ").lower()
    skip_dns = skip_dns_input == 'y'

    max_hops_input = input("Set max hops (press Enter to use default 30): ")
    max_hops = int(max_hops_input) if max_hops_input else 30

    timeout_input = input("Set timeout in ms (press Enter to use default 4000): ")
    timeout = int(timeout_input) if timeout_input else 4000

    command = ['tracert']
    if skip_dns:
        command.append('-d')
    command += ['-h', str(max_hops), '-w', str(timeout), target]

    print(f"\nRunning command: {' '.join(command)}")
    try:
        output = subprocess.check_output(command, text=True)
        print(output)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.output}")

def header_grabber():
    url = input("Enter a website URL (without http/https): ")
    if not url.startswith("http"):
        url = "http://" + url
    print(f"\nFetching HTTP headers for {url}...")
    try:
        response = requests.get(url, timeout=5)
        print("\nServer Headers:")
        for header, value in response.headers.items():
            print(f"{header}: {value}")
    except Exception as e:
        print(f"Error fetching headers: {e}")

def get_external_ip():
    print("\nGetting External IP Address...")
    try:
        ip = requests.get('https://api.ipify.org', timeout=5).text
        print(f"Your External IP Address is: {ip}")
    except Exception as e:
        print(f"Error fetching external IP: {e}")

def dns_lookup():
    domain = input("Enter domain for DNS lookup: ")
    try:
        ip = socket.gethostbyname(domain)
        print(f"IP Address of {domain}: {ip}")
    except socket.gaierror:
        print("DNS Lookup failed.")

if __name__ == "__main__":
    while True:
        show_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            wifi_networks()
        elif choice == '2':
            internet_speed_test()
        elif choice == '3':
            own_ip_geolocation()
        elif choice == '4':
            any_ip_geolocation()
        elif choice == '5':
            ping_website()
        elif choice == '6':
            traceroute()
        elif choice == '7':
            header_grabber()
        elif choice == '8':
            get_external_ip()
        elif choice == '9':
            dns_lookup()
        elif choice == '10':
            show_manual()
        elif choice == '0':
            print("Exiting. Thank you!")
            break
        else:
            print("Invalid choice. Please try again.")
