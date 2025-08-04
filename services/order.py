from datetime import datetime
from db.models import Order, Ticket, User, MovieSession
from django.db.models import QuerySet
from django.db import transaction


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> Order | None:
    user = User.objects.get(username=username)
    with transaction.atomic():
        order_info = {"user": user}
        if date:
            if isinstance(date, str):
                date = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order_info["created_at"] = date
        order = Order.objects.create(**order_info)
        for ticket_info in tickets:
            movie_session_id = ticket_info["movie_session"]
            movie_session = MovieSession.objects.get(id=movie_session_id)
            ticket_data_for_creating = ticket_info.copy()
            ticket_data_for_creating.pop("movie_session")
            Ticket.objects.create(
                order=order,
                movie_session=movie_session,
                **ticket_data_for_creating)
        return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
