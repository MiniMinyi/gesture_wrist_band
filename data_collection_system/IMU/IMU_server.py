import smbus
import math
import time
import flask
import json

app = flask.Flask(__name__)
log_file = open("/home/pi/IMU/log.txt", 'a')

# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c


def read_byte(reg):
    return bus.read_byte_data(address, reg)


def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg + 1)
    value = (h << 8) + l
    return value


def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val


def dist(a, b):
    return math.sqrt((a * a) + (b * b))


def get_y_rotation(x, y, z):
    radians = math.atan2(x, dist(y, z))
    return -math.degrees(radians)


def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)


bus = smbus.SMBus(1)  # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68  # via i2cdetect


@app.route('/get_IMU_data/<timestamp>')
def get_IMU_data(timestamp):
    # Aktivieren, um das Modul ansprechen zu koennen
    bus.write_byte_data(address, power_mgmt_1, 0)

    # print "Gyroskop"
    # print "--------"

    gyroskop_xout = read_word_2c(0x43)
    gyroskop_yout = read_word_2c(0x45)
    gyroskop_zout = read_word_2c(0x47)

    # gyroskop_xout = gyroskop_xout / 131
    # gyroskop_yout = gyroskop_yout / 131
    # gyroskop_zout = gyroskop_zout / 131

    beschleunigung_xout = read_word_2c(0x3b)
    beschleunigung_yout = read_word_2c(0x3d)
    beschleunigung_zout = read_word_2c(0x3f)

    beschleunigung_xout_skaliert = beschleunigung_xout / 16384.0
    beschleunigung_yout_skaliert = beschleunigung_yout / 16384.0
    beschleunigung_zout_skaliert = beschleunigung_zout / 16384.0
    response = flask.jsonify({"gyro": [gyroskop_xout, gyroskop_yout, gyroskop_zout],
                              "acc": [beschleunigung_xout_skaliert, beschleunigung_yout_skaliert,
                                      beschleunigung_zout_skaliert]})

    log_file.write("%s %.8f %.8f %.8f %d %d %d\n" % (
    timestamp, beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert, gyroskop_xout,
    gyroskop_yout, gyroskop_zout))
    log_file.flush()

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=8888)
