menu_options = {
    1: 'Enter an IP address to make calculations',
    2: 'Matching prefix to mask',
    3: 'Exit'
}


def print_menu():
    for option in menu_options.keys():
        print(option, "-", menu_options[option])


def print_table(dict, isbin=False):
    # Output all calculated information to a console
    for element in dict:
        print("-----------------------------------------------------------")
        if type(dict[element]) is list:
            print(element, end=" - ")
            delimiter = "."
            for octet in range(4):
                if octet == 3:
                    delimiter = "\n"
                if isbin == False:
                    print(f"{str(dict[element][octet])}", end=delimiter)
                else:
                    print("{:08b}".format(dict[element][octet]), end=delimiter)
        else:
            print(element, f" - {dict[element]}")


def prefix_mask_matching(prefix):
    # Convert a network prefix value into a network mask
    bit_mask = [0] * 32
    for i in range(prefix):
        bit_mask[i] = 1
    # Сonverting a list of bits into a list of mask octets
    bit_mask = [bit_mask[octet*8:(octet+1)*8] for octet in range(4)]
    bit_mask = [[str(bit) for bit in octet] for octet in bit_mask]
    bit_mask = ["".join(octet) for octet in bit_mask]
    dec_mask = [int(octet, 2) for octet in bit_mask]
    return dec_mask


def list_prefixes_masks_matching():
    # Matching all possible options of prefixes with network masks and
    # output results to a console
    for prefix in range(33):
        first_octet, second_octet, third_octet, fourth_octet = prefix_mask_matching(prefix)
        print(f"/{prefix} - {first_octet}.{second_octet}.{third_octet}.{fourth_octet}")


def get_ip_address():
    # Getting and validating value of IP address entered from a console
    while True:
        ip_addr = input("Enter an IP address: ")
        ip_addr_error = f"This address {ip_addr} is not valid!"
        error_presence = 0
        try:
            octets = ip_addr.split(".")
            octets = list(map(int, octets))
        except:
            print(ip_addr_error)
            continue

        if len(octets) != 4:
            print(ip_addr_error)
            continue
        for octet in octets:
            if octet < 0 or octet > 255:
                print(ip_addr_error)
                error_presence = 1
                break

        if error_presence == 0:
            break
    return octets


def get_network_prefix():
    # Getting and validating value of network prefix entered from a console
    while True:
        try:
            net_prefix = int(input("Enter a network prefix: "))
            if net_prefix < 0 or net_prefix > 32:
                print(f"This network prefix is not valid!")
                continue
        except:
            print(f"This network prefix is not valid!")
            continue
        break
    return net_prefix


def network_calc(ip_addr, prefix):
    # Network address calculation
    mask = prefix_mask_matching(prefix)
    network = [ip_addr[octet] & mask[octet] for octet in range(4)]
    return network


def broadcast_calc(ip_addr, prefix):
    mask = prefix_mask_matching(prefix)
    reverse_mask = [mask[octet] ^ 0b11111111 for octet in range(4)]
    broadcast = [ip_addr[octet] | reverse_mask[octet] for octet in range(4)]
    return broadcast


def first_host_calc(ip_addr, prefix):
    first_host = network_calc(ip_addr, prefix)
    first_host[3] += 1
    return first_host


def last_host_calc(ip_addr, prefix):
    last_host = broadcast_calc(ip_addr, prefix)
    last_host[3] -= 1
    return last_host


def count_hosts(prefix):
    return 2**(32-prefix) - 2


def network_summary(ip_addr, prefix):
    network_sum = {
        "IP address": ip_addr,
        "Mask": prefix_mask_matching(prefix),
        "Network": network_calc(ip_addr, prefix),
        "Broadcast": broadcast_calc(ip_addr, prefix),
        "First Host Address": first_host_calc(ip_addr, prefix),
        "Last Host Address": last_host_calc(ip_addr, prefix),
        "Ammount of hosts/networks": count_hosts(prefix)
    }
    return network_sum


if __name__ == '__main__':
    while True:
        print("\nMenu:")
        print_menu()
        try:
            option = int(input("Your choice: "))
        except:
            print("Wrong input. Please enter a number.")

        if option == 1:
            ip_address = get_ip_address()
            ip_prefix = get_network_prefix()
            net_sum = network_summary(ip_address, ip_prefix)
            print_table(net_sum)
            print_table(net_sum, isbin=True) # Repeated output of information, but in binary form

        elif option == 2:
            list_prefixes_masks_matching()
        elif option == 3:
            exit()
