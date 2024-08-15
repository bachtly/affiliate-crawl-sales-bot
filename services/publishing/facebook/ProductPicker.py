from utils.logger.logging import ErrorLogger


class ProductPicker:
    @staticmethod
    def pick(publishTimes):
        if len(publishTimes) == 0:
            e = Exception("ProductPicker.pick.empty_publishTimes")
            ErrorLogger.error(str(e))
            return None, e

        publishTimes = publishTimes
        publishTimes = dict(sorted(publishTimes.items(), key=lambda item: item[1]))

        productId = list(publishTimes.items())[0][0]

        return productId, None
