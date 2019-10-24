import Display
import pyaudio
import numpy as np
import math


def soundplot(s, display_window):
    # Read stream data
    data = np.frombuffer(s.read(CHUNK), dtype=np.int16)

    # Perform a Fast Fourier Transform, then split the resulting list by the width of the display screen
    p = split_avg(np.log10(np.abs(np.fft.rfft(data))), display_window.width)
    f = np.linspace(0, RATE/2, len(p))
    for i in range(len(f)):
        display_window.freq_assign(i, p[i]/7-0.1)


def split_avg(m_list, x):

    # The size of each grouping
    sub_list_group_size = len(m_list)/x

    # The accumulation of our carry over values from each time we group
    remainder_acc = 0.0

    # The remainder of value not accounted in each base grouping. IE 100/3 doesnt divide very well
    # but we still need to account for those extra values so that all are included
    # and we come out as close to 3 groups as possible
    remainder = sub_list_group_size - sub_list_group_size//1

    # Reassign this value to it's floor amount
    sub_list_group_size = int(math.floor(sub_list_group_size))

    # Our return list
    new_list = []

    # Range not used as we need to manually be able to bump i higher when our remainder accumulation rolls over 1
    # The rest is just magic, but it works
    i = 0
    while i < len(m_list):
        remainder_acc += remainder
        carry_base = int(remainder_acc//1)
        l = m_list[i:i+sub_list_group_size+carry_base]
        new_list.append(sum(l)/len(l))
        i += carry_base
        remainder_acc -= carry_base
        i += sub_list_group_size

    return new_list[:x]


def get_default_device(p):

    compatible_devices = []

    try:
        default_device_index = p.get_default_output_device_info()["index"]
    except IOError:
        default_device_index = -1

    for i in range(0, p.get_device_count()):
        info = p.get_device_info_by_index(i)
        api = p.get_host_api_info_by_index(info["hostApi"])["name"]

        if api == 'Windows WASAPI':
            print(f'{info["index"]}: {info["name"]}')
            compatible_devices.append((info["index"], info["name"]))

    if default_device_index in compatible_devices:
        return default_device_index

    default_name = p.get_device_info_by_index(default_device_index)["name"]

    i=0

    while len(compatible_devices) != 1:
        i += 1
        for o in range(len(compatible_devices)):
            try:
                index, name = compatible_devices[o]
                print(f'{index}: {name}')
                if str(name)[0:i] != str(default_name)[0:i]:
                    del compatible_devices[o]
            except IndexError:
                pass

    return compatible_devices[0][0]


if __name__ == "__main__":

    RATE = 48000
    CHUNK = 1024
    disp = Display.EQ(68, resize=False)

    # Instantiate our PyAudio
    p = pyaudio.PyAudio()
    our_device = get_default_device(p)
    # Open our audio stream
    # TODO self-assign default audio
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    as_loopback=True,
                    input_device_index=our_device)

    disp.display()
    # Keep pulling audio until keyboard interrupt
    while True:
        try:
            soundplot(stream, disp)
        except KeyboardInterrupt:
            disp.stop_display()
            break

    stream.stop_stream()
    stream.close()
    p.terminate()
