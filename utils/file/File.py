from utils.scheduler.Scheduler import Scheduler


class File:
    @staticmethod
    def GetLogPhotoFileDir(caller, filename):
        filename = f'log/{getattr(Scheduler.threadLocal, "flow")}/' \
                   + f'{caller.__class__.__name__}/' \
                   + filename
        return filename
