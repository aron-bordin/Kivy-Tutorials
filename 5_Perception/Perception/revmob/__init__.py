from kivy.utils import platform
from kivy.logger import Logger

Logger.info('Loading RevMob module')
if platform() == 'android':
    from .android import *
elif platform() == 'ios':
    from .ios import *
else:
    Logger.warning('[RevMob] Unkown platform: %s' % platform())
