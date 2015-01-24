import ctypes
from pyobjus import autoclass

print("Loading RevMob iOS SDK")

ctypes.CDLL('./RevMobAds.a')
RevMobNative = autoclass('RevMobAds')

ns = lambda x: NSString.alloc().initWithUTF8String_(x)

RevMobNative = autoclass('RevMobAds')

TESTING_MODE_DISABLED = 0
TESTING_MODE_WITH_ADS = 1
TESTING_MODE_WITHOUT_ADS = 2


class RevMob(object):
    TESTING_MODE_DISABLED = RevMobTestingMode.DISABLED
    TESTING_MODE_WITH_ADS = RevMobTestingMode.WITH_ADS
    TESTING_MODE_WITHOUT_ADS = RevMobTestingMode.WITHOUT_ADS

    @staticmethod
    def start_session(app_id):
        RevMobNative.startSessionWithAppID(ns(app_id))

    @staticmethod
    def show_fullscreen():
        RevMobNative.session().showFullscreen()

    @staticmethod
    def show_popup():
        RevMobNative.session().showPopup()

    @staticmethod
    def open_link():
        RevMobNative.session().openAdLink()

    @staticmethod
    def set_testing_mode(mode):
        RevMobNative.session().setTestingMode(mode)

    @staticmethod
    def print_environment_information():
        RevMobNative.session().printEnvironmentInformation()

