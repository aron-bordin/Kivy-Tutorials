from jnius import autoclass

print("Loading RevMob Android SDK")

RevMobNative = autoclass('com.revmob.RevMob')
RevMobTestingMode = autoclass('com.revmob.RevMobTestingMode')
PythonActivity = autoclass('org.renpy.android.PythonActivity')

TESTING_MODE_DISABLED = RevMobTestingMode.DISABLED
TESTING_MODE_WITH_ADS = RevMobTestingMode.WITH_ADS
TESTING_MODE_WITHOUT_ADS = RevMobTestingMode.WITHOUT_ADS


class RevMob(object):
    __session = None
    TESTING_MODE_DISABLED = RevMobTestingMode.DISABLED
    TESTING_MODE_WITH_ADS = RevMobTestingMode.WITH_ADS
    TESTING_MODE_WITHOUT_ADS = RevMobTestingMode.WITHOUT_ADS

    @staticmethod
    def start_session(app_id):
        if not RevMob.__session:
            RevMob.__session = RevMobNative.start(PythonActivity.mActivity, app_id)

    @staticmethod
    def show_fullscreen():
        if RevMob.__session:
            RevMob.__session.showFullscreen(PythonActivity.mActivity, None, None)

    @staticmethod
    def show_popup():
        if RevMob.__session:
            RevMob.__session.showPopup(PythonActivity.mActivity, None, None)

    @staticmethod
    def open_link():
        if RevMob.__session:
            RevMob.__session.openAdLink(PythonActivity.mActivity, None, None)

    @staticmethod
    def set_testing_mode(mode):
        if RevMob.__session:
            RevMob.__session.setTestingMode(mode)

    @staticmethod
    def print_environment_information():
        if RevMob.__session:
            RevMob.__session.printEnvironmentInformation(PythonActivity.mActivity)

