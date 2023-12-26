# device details and configuration of app key

import board
import busio
import digitalio
import time
import microcontroller

uart = busio.UART(board.GP4, board.GP5, baudrate=9600, timeout=20)

#lastSeconds = time.time()
#lastSeconds = 0
#diffSeconds = 0
#seconds = 0



def setup():
    print("LoRa IDs:", lora_get_ids())

    # Setting the LoRa datarate is only required once, will be stored
    print(lora_set_datarate())

    # Setting the LoRa Appkey is only required once, will be stored
    #print(lora_set_appkey(b"APP_KEY_FROM_THINGS_CONSOLE"))
    #print(lora_set_appkey(b"E9F8DE090597303DC8045046458D1BA2"))
    print(lora_set_appkey(b"8460A85D9E3750B7D076F4A5F621A6BF"))

    ##seconds = time.time()
    #diffSeconds = seconds - lastSeconds
    ##print ("Seconds since epoch = ", seconds)	# ok
    #print ("Seconds since epoch = ", diffSeconds)	# ok
    #lastSeconds = seconds

    # convert the time in seconds since the epoch to a readable format
    #local_time = time.ctime(seconds)

    #print("Local time:", local_time)
 
    #named_tuple = time.localtime() # get struct_time
    #time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)

    #print(time_string)

    print(" setup finished ")

def at_send(cmd, max_time=10):
    if not isinstance(cmd, bytes):
        print("cmd must be a byte string, terminated with new line")
        return ""

    now = time.monotonic()
    uart.write(cmd)
    result = ""
    while True:
        byte_read = uart.readline() # read one line
        if byte_read == None: # no more response
            break

        response = byte_read.decode()
        result += response
        if (time.monotonic() - now) > max_time:
            print("reached at_send max_time", max_time)
            break

    return result

# return dict with the ids
# LoRa IDs: {'AppEui': '52:69:73:69:6E:67:48:46', 'DevAddr': '50:20:AA:44', 'DevEui': '2C:F7:F1:20:50:20:AA:44'}
def lora_get_ids():
    response = at_send(b"AT+ID\n")
    result = {
        #"DevAddr": "5020AA44",
        "DevAddr": "",
        #"DevEui": "70B3D57ED0062946",
        "DevEui": "",
        #"AppEui": "52:69:73:69:6E:67:48:46",
        "AppEui": "",
    }
    for line in response.splitlines():
        for key in result.keys():
            if key in line:
                result[key] = line.split(",")[1].strip()

    return result

def lora_get_datarate():
    result_string = at_send(b"AT+DR\n")
    return result_string

def lora_set_datarate():
    # TODO(yw): should accept
    result_string = at_send(b"AT+DR=5\n")
    return result_string

def lora_join():
    result_string = at_send(b"AT+JOIN\n", 10)
    return result_string

def lora_set_appkey(appkey):
    result_string = at_send(b"AT+KEY=APPKEY," + appkey + "\n", 10)
    return result_string

def lora_send_text(msg, with_confirmation=True):
    payload = b""
    downstream_messages = []
    if isinstance(msg, str):
        userinput = msg.strip()
        payload = bytes(userinput, "utf-8")
    else:
        print("Please provide a string")
        return

    cmd = b"AT+CMSG=\""
    if with_confirmation == False:
        cmd = b"AT+MSG=\""

    cmd = cmd + payload + b"\"\n"
    response = at_send(cmd, 10)
    return response

setup()

response = lora_join()
print (response)

while True:
    temp = microcontroller.cpu.temperature
    print ("temperature intern : ") 
    print (str(temp)) 
    response = lora_send_text(str(temp))
    print (response)
    time.sleep(300) 

