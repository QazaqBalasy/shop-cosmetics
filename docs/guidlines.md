* admin/
  Admin page to manage your db.
* ^api/login/
  Get the token and user info:
  - api/login/social/token
  Get only token:
  - api/login/social/token_user
* me/
  [GET]
  Get the user info.
  Include token of the user in HEADERS
* cosmetic-categories/
  [Get]
  Get categories of cosmetics.
  Get specific category:
  - cosmetic-categories/<int:pk>/
  - search by name:
    cosmetic-categories/?search=Hand
  - ordering by name:
    cosmetic-categories/?ordering=-name
    cosmetic-categories/?ordering=name
* cosmetics/
  [GET]
  cosmetic-list.
  cosmetic-detail:
    - cosmetics/<int:pk>/
  - search by name:
  - ordering by name or price:
* cosmetics/<int:pk>/add/
  [POST]
  Add cosmetics to your basket.First create an order.
  Include token of the user in HEADERS
* orders/<int:order_pk>/cosmetics/
  [GET]
  basket list
* orders/<int:order_pk>/cosmetics/<int:cosmetic_pk>/
  [GET,PATCH,DELETE]
  Get or delete your cosmetics in the basket.
  Include token of the user in HEADERS
* orders/
  [GET]
  order-list
  [POST]
  Create an order.Only one order could be active(not confirmed)
  - ordering by date_added, date_updated, confirmation_date
  Include token of the user in HEADERS
* orders/<int:pk>/
  [GET]
  Order-detail.
  [PATCH]
  You can include fields in body to change the order info.
  Include token of the user in HEADERS
* confirmed-orders/
  [GET]
  Confirmed orders list
  - ordering by date_added, date_updated, confirmation_date
  Include token of the user in HEADERS
* confirmed-orders/<int:pk>/
  [GET]
  Confirmed order detail.
  Include token of the user in HEADERS
* favorites/
  [GET]
  Favorites list .
  Include token of the user in HEADERS
* Favorites/<int:pk>/
  [DELETE]
  Favorites delete.
  Include token of the user in HEADERS
* cosmetics/<int:pk>/add-favorite/
  [POST]
  Also add pk(aka id) of cosmetics in your BODY to add it to fav.Otherwise error will raise.
  Include token of the user in HEADERS
* bankcards/add/.
  [POST]
  Add a bank card.
  [GET]
  List of bankcards:
  - bankcards/
  [DELETE] bank card
  - bankcards/<int:pk>
  Include token of the user in HEADERS
