from pydantic import BaseModel

class ZenicogBaseModel(BaseModel):
    """
    모든 스키마 클래스가 기본적으로 `extra = "ignore"` 설정을 상속받도록 하는 베이스 클래스.
    이 모델을 상속하면, JSON에 선언되지 않은 필드가 와도 자동으로 무시됩니다.
    """
    class Config:
        extra = "ignore"
