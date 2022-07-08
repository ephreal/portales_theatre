# This is a VERY simple test since there is nothing to test yet.
# If everything is working as expected, we'll get a bunch of
# 200 ok responses.

curl -X GET localhost:5001/api/admin/play/1
curl -H "Content-Type: application/json" -d '{"date": "2022-01-01", "seats": {}}' -X PUT localhost:5001/api/admin/play/1
curl -X DELETE localhost:5001/api/admin/play/2
curl -H "Content-Type: application/json" -d '{"date": "2021-01-01", "seats": {}, "name": "Phantom of the Parking Lot", "description": "A long lost tale of love and romance from a parking lot far far away (it was Walmart)"}' -X POST localhost:5001/api/admin/play/
curl -X GET localhost:5001/api/admin/seat/2
curl -H "Content-Type: application/json" -d '{"row": 2, "column": 1, "id": 2, "price": 25}' -X PUT localhost:5001/api/admin/seat/2
curl -X DELETE localhost:5001/api/admin/seat/1
curl -H "Content-Type: application/json" -d '{"row": 0, "column": 0, "play": 1, "price": 256.3}' -X POST localhost:5001/api/admin/seat/
curl -X GET localhost:5001/api/client/play/1
curl -X PUT localhost:5001/api/client/play/1
curl -X DELETE localhost:5001/api/client/play/1
curl -X POST localhost:5001/api/client/play/
curl -X GET localhost:5001/api/client/seat/1
curl -H "Content-Type: application/json" -d '{"available": false, "row": 2, "column": 1, "id": 2, "price": 25}' -X PUT localhost:5001/api/client/seat/1
curl -X DELETE localhost:5001/api/client/seat/1
curl -X POST localhost:5001/api/client/seat/
