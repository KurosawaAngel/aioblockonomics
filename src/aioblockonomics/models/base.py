from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict


class BaseBlockonomicsModel(_BaseModel):
    model_config = ConfigDict(frozen=True)
