from typing import Iterable

from dishka import AsyncContainer, Provider, make_async_container

from core.config import Config, create_config


def create_async_container(providers: Iterable[Provider], config: Config) -> AsyncContainer:
    return make_async_container(*providers, context={Config: config})
