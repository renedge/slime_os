import slime_os.launcher
from slime_os.graphics import *
from slime_os.expansion import *
from slime_os.intents import *
from slime_os.keycode import Keycode as keycode
from config import config


TMP_DOWNLOAD_PLAY_APP = "/sd/download_play_app.py"


def get_internal_i2c():
    return hardware.I2C(1, scl=hardware.Pin(7), sda=hardware.Pin(6))


def get_expansion_i2c():
    return hardware.I2C(1, scl=hardware.Pin(1), sda=hardware.Pin(0))


def get_expansion_uart(baudrate=115200):
    return hardware.UART(0, baudrate, tx=hardware.Pin(0), rx=hardware.Pin(1))


def get_sdcard():
    sd_spi = hardware.SPI(
        1,
        sck=hardware.Pin(10, hardware.Pin.OUT),
        mosi=hardware.Pin(11, hardware.Pin.OUT),
        miso=hardware.Pin(12, hardware.Pin.OUT),
    )
    return hardware.sdcard.SDCard(sd_spi, hardware.Pin(15))


def get_applications() -> list[dict[str, str, str]]:
    applications = []
    global app

    app_dir = "apps"

    app_files = hardware.os.listdir(app_dir)
    download_play_app = TMP_DOWNLOAD_PLAY_APP

    for file in app_files:
        if file.endswith("app.py"):
            applications.append(
                {
                    "file": file[:-3],
                }
            )

    try:
        hardware.os.stat(download_play_app)  # Get file information
        applications.append({"file": download_play_app[:-3], "temporary": True})
    except OSError:
        pass

    for app in applications:
        frontmatter = ""
        filename = app_dir + "/" + app["file"] + ".py"
        with hardware.open(filename, "r") as f:
            index = 0
            for line in f.readlines():
                if index == 0:
                    if not line.startswith('"'):
                        print(line)
                        print(f"[APP].MISSING_METADATA {name}")
                        break
                if index > 0:
                    if not line.startswith('"'):
                        frontmatter += line
                    else:
                        break
                index += 1
            f.close()

        try:
            exec(frontmatter)
        except SyntaxError:
            print(f"[APP].SYNTAX_ERROR {name}")

    return sorted(applications, key=lambda x: x["name"])


hardware = config["modules"]["hardware"](locals())
display = config["modules"]["display"](locals())
graphics = Gfx(display)
keyboard = config["modules"]["keyboard"](locals())
ctrl = Ctrl(locals())

sd = hardware.sdcard.get_sdcard()
hardware.os.mount(sd, "/sd")

persist = {}

try:
    hardware.os.remove(TMP_DOWNLOAD_PLAY_APP)
    print("[sos].temp_file_removed")
except:
    print("[sos].temp_file_missing")


def boot(next_app):
    for key, color in config["theme"].items():
        if isinstance(color, tuple):
            config["theme"][key] = graphics.create_pen(*color)

    running_app = next_app()
    running_app_instance = None

    while True:
        display.tick()
        if running_app:
            if not running_app_instance:
                running_app.setup(graphics)
                running_app_instance = running_app.run()
            intent = next(running_app_instance)
        else:
            intent = INTENT_FLIP_BUFFER

        if is_intent(intent, INTENT_KILL_APP):
            running_app = None
            running_app_instance = None
            print("[SOS].APP_KILLED")
            hardware.gc.collect()

            next_app = launcher.App
            if len(intent) == 2:
                next_app = __import__(intent[1]["file"]).App
            running_app = next_app()

        if is_intent(intent, INTENT_NO_OP):
            pass

        if is_intent(intent, INTENT_FLIP_BUFFER):
            graphics.set_pen(config["theme"]["black"])
            graphics.rectangle(0, 0, display.width, 40)
            graphics.set_pen(config["theme"]["white"])
            graphics.line(display.width - 12, 40, display.width - 12 - 120, 40)
            graphics.line(0 + 12, 40, 0 + 12 + 120, 40)

            window_title = "SLIMEDECK ZERO"

            graphics.text(window_title, display.width - 12 - 10, 31, -1, 1, 180)
            graphics.text(free(), 0 + 12 + 86, 31, -1, 1, 180)
            graphics.update()


def prepare_for_launch() -> None:
    for k in locals().keys():
        if k not in ("__name__", "gc"):
            del locals()[k]
    hardware.gc.collect()


def free(full=False):
    hardware.gc.collect()
    F = hardware.gc.mem_free()
    A = hardware.gc.mem_alloc()
    T = F + A
    P = "MEM USAGE {0:.2f}%".format(100 - (F / T * 100))
    if not full:
        return P
    else:
        return "T:{0} F:{1} ({2})".format(T, F, P)


if __name__ == "__main__":
    boot(slime_os.launcher.App)
