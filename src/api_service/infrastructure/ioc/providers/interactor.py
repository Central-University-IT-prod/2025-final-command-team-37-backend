from dishka import Provider, Scope, provide_all

from domain.interactors.auth import (
    GenerateAccessTokenInteractor,
    OAuth2PasswordBearerInteractor,
)
from domain.interactors.user import (
    GetUserInteractor,
    ListUserInteractor,
    AddUserInteractor,
)
from domain.interactors.coworking import (
    GetCoworkingInteractor,
    ListCoworkingsInteractor,
    AddCoworkingInteractor,
    UpdateCoworkingInteractor,
    DeleteCoworkingInteractor,
    AddCoworkingTariffsInteractor,
    ListCoworkingTariffsInteractor,
)
from domain.interactors.workplace import (
    UpsertWorkplacesInteractor,
    ListWorkplacesInteractor,
)
from domain.interactors.booking import (
    GetBookingInteractor,
    ListUserBookingsInteractor,
    ListCoworkingBookingsInteractor,
    ListAllBookingsInteractor,
    AddBookingInteractor,
    UpdateBookingInteractor,
    DeleteBookingInteractor,
    ActivateBookingInteractor,
    PendingBookingsInteractor,
)
from domain.interactors.stats import (
    StatsCoworkingCountInteractor,
    StatsWorkplacesCountInteractor,
    StatsMediumPricePerHourInteractor,
    StatsOccupancyRateInteractor,
)
from domain.interactors.cdn import (
    SaveImageInteractor,
    GetImageInteractor,
)
from domain.interactors.external import (
    AddTgAdminInteractor,
    RemoveTgAdminInteractor,
)


class InteractorProvider(Provider):
    scope = Scope.REQUEST

    auth_interactor = provide_all(
        GenerateAccessTokenInteractor,
        OAuth2PasswordBearerInteractor,
    )

    user_interactor = provide_all(
        GetUserInteractor,
        ListUserInteractor,
        AddUserInteractor,
    )

    coworking_interactor = provide_all(
        GetCoworkingInteractor,
        ListCoworkingsInteractor,
        AddCoworkingInteractor,
        UpdateCoworkingInteractor,
        DeleteCoworkingInteractor,
        AddCoworkingTariffsInteractor,
        ListCoworkingTariffsInteractor,
    )

    workplace_interactor = provide_all(
        UpsertWorkplacesInteractor,
        ListWorkplacesInteractor,
    )

    booking_interactor = provide_all(
        GetBookingInteractor,
        ListUserBookingsInteractor,
        ListCoworkingBookingsInteractor,
        ListAllBookingsInteractor,
        AddBookingInteractor,
        UpdateBookingInteractor,
        DeleteBookingInteractor,
        ActivateBookingInteractor,
        PendingBookingsInteractor,
    )

    stats_interactor = provide_all(
        StatsCoworkingCountInteractor,
        StatsWorkplacesCountInteractor,
        StatsMediumPricePerHourInteractor,
        StatsOccupancyRateInteractor,
    )

    cdn_interactor = provide_all(
        SaveImageInteractor,
        GetImageInteractor,
    )

    external_interactor = provide_all(
        AddTgAdminInteractor,
        RemoveTgAdminInteractor,
    )
