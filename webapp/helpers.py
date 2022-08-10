from dataclasses import dataclass, field

from flask import url_for


@dataclass
class ApiEndpoint:
    """
    This class helps us to generate our API page.
    """
    model: str
    title: str
    handle: str
    method: str
    template: str
    default_params: dict = field(default_factory=dict)

    def url(self):
        if self.default_params:
            return url_for(self.handle, **self.default_params)
        else:
            return url_for(self.handle)