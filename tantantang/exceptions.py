class BusinessException(Exception):
    """项目基础异常类"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
