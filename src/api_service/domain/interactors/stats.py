from domain.gateway import StatsGateway


class StatsCoworkingCountInteractor:
    def __init__(self, stats_gateway: StatsGateway):
        self.stats_gateway = stats_gateway

    async def __call__(self) -> int:
        coworking_count = await self.stats_gateway.get_coworking_count()
        return coworking_count


class StatsWorkplacesCountInteractor:
    def __init__(self, stats_gateway: StatsGateway):
        self.stats_gateway = stats_gateway

    async def __call__(self) -> int:
        workplaces_count = await self.stats_gateway.get_workplaces_count()
        return workplaces_count


class StatsMediumPricePerHourInteractor:
    def __init__(self, stats_gateway: StatsGateway):
        self.stats_gateway = stats_gateway

    async def __call__(self) -> float:
        medium_price_per_hour = await self.stats_gateway.get_medium_price_per_hour()
        return medium_price_per_hour


class StatsOccupancyRateInteractor:
    def __init__(self, stats_gateway: StatsGateway):
        self.stats_gateway = stats_gateway

    async def __call__(self) -> float:
        occupancy_rate = await self.stats_gateway.get_occupancy_rate()
        return occupancy_rate
